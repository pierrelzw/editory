#!/usr/bin/env python3
"""Upload local files to Mowen via their two-step REST API.

Step 1: Call the prepare endpoint to get OSS upload fields.
Step 2: POST the file as multipart/form-data to the OSS endpoint.

Usage:
    python3 scripts/upload_to_mowen.py cover.png
    python3 scripts/upload_to_mowen.py img1.png img2.jpg --pretty
    MOWEN_API_KEY=xxx python3 scripts/upload_to_mowen.py file.pdf
"""

import json
import os
import sys
import time
from pathlib import Path

import requests

PREPARE_URL = "https://open.mowen.cn/api/open/api/v1/upload/prepare"

# Extension → fileType mapping (1=image, 2=audio, 3=pdf)
EXT_TO_FILETYPE = {
    ".jpg": 1,
    ".jpeg": 1,
    ".png": 1,
    ".gif": 1,
    ".webp": 1,
    ".mp3": 2,
    ".m4a": 2,
    ".mp4": 2,
    ".pdf": 3,
}


def detect_filetype(filename: str) -> int | None:
    """Return Mowen fileType int from file extension, or None if unknown."""
    ext = Path(filename).suffix.lower()
    return EXT_TO_FILETYPE.get(ext)


def prepare_upload(api_key: str, filename: str, filetype: int) -> dict:
    """Call the prepare endpoint to get OSS upload fields.

    Returns the full JSON response which should contain:
    - A `form` object with OSS fields (key, policy, callback, signature, etc.)
    - An `endpoint` or `host` field for the OSS upload URL
    """
    resp = requests.post(
        PREPARE_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"fileType": filetype, "fileName": filename},
        timeout=30,
    )
    resp.raise_for_status()
    body = resp.json()

    # The API wraps results in a `data` field in some versions
    if "data" in body and isinstance(body["data"], dict):
        return body["data"]
    return body


def extract_endpoint(prepare_data: dict) -> str:
    """Extract the OSS upload endpoint URL from the prepare response.

    Alibaba Cloud OSS pattern: the endpoint is typically a separate field
    outside the `form` object. We check several common field names.
    """
    # Check top-level fields first
    for key in ("endpoint", "host", "url", "uploadUrl", "upload_url"):
        if key in prepare_data and prepare_data[key]:
            return prepare_data[key]

    # Check inside the form object as fallback
    form = prepare_data.get("form", {})
    for key in ("endpoint", "host", "url"):
        if key in form and form[key]:
            return form[key]

    raise ValueError(
        "Cannot find upload endpoint in prepare response. "
        f"Available keys: {list(prepare_data.keys())}"
    )


def upload_file(api_key: str, filepath: Path) -> dict:
    """Upload a single file to Mowen. Returns result dict with uuid."""
    filename = filepath.name
    filetype = detect_filetype(filename)
    if filetype is None:
        raise ValueError(f"Unsupported file extension: {filepath.suffix}")

    # Step 1: Prepare — get OSS upload fields
    prepare_data = prepare_upload(api_key, filename, filetype)
    endpoint = extract_endpoint(prepare_data)
    form_fields = prepare_data.get("form", {})

    # Step 2: Upload to OSS endpoint with all form fields + file binary
    # Order matters for some OSS providers: fields first, file last
    multipart_fields = []
    for key, value in form_fields.items():
        multipart_fields.append((key, (None, str(value))))

    with filepath.open("rb") as fh:
        multipart_fields.append(
            ("file", (filename, fh, "application/octet-stream"))
        )
        resp = requests.post(endpoint, files=multipart_fields, timeout=120)

    resp.raise_for_status()

    try:
        result = resp.json()
    except requests.exceptions.JSONDecodeError:
        raise ValueError(
            f"OSS returned non-JSON response (status {resp.status_code}): "
            f"{resp.text[:200]}"
        )

    # Extract UUID — may be nested in `data` or at top level
    uuid = None
    if isinstance(result, dict):
        uuid = result.get("uuid") or result.get("fileId") or result.get("file_id")
        if not uuid and "data" in result and isinstance(result["data"], dict):
            data = result["data"]
            uuid = data.get("uuid") or data.get("fileId") or data.get("file_id")

    if not uuid:
        raise ValueError(
            f"UUID not found in OSS response. Keys: {list(result.keys()) if isinstance(result, dict) else type(result)}"
        )

    return {
        "uuid": uuid,
        "fileName": filename,
        "fileType": filetype,
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Upload files to Mowen via REST API"
    )
    parser.add_argument(
        "files", nargs="+", help="File paths to upload"
    )
    parser.add_argument(
        "--pretty", action="store_true", help="Pretty-print JSON output"
    )
    args = parser.parse_args()

    api_key = os.environ.get("MOWEN_API_KEY", "").strip()
    if not api_key:
        print(
            "Error: MOWEN_API_KEY environment variable is required.\n"
            "Set it with: export MOWEN_API_KEY=your_api_key",
            file=sys.stderr,
        )
        sys.exit(1)

    indent = 2 if args.pretty else None
    has_failure = False

    for i, filepath_str in enumerate(args.files):
        filepath = Path(filepath_str)
        if not filepath.is_file():
            print(f"Error: file not found: {filepath}", file=sys.stderr)
            has_failure = True
            continue

        try:
            result = upload_file(api_key, filepath)
            print(json.dumps(result, ensure_ascii=False, indent=indent))
        except Exception as e:
            print(f"Error uploading {filepath}: {e}", file=sys.stderr)
            has_failure = True

        # Rate limit: 1 req/sec between files in batch mode
        if i < len(args.files) - 1:
            time.sleep(1)

    sys.exit(1 if has_failure else 0)


if __name__ == "__main__":
    main()
