"""Tests for upload_to_mowen.py — local file upload to Mowen via REST API."""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from upload_to_mowen import (
    detect_filetype,
    extract_endpoint,
    prepare_upload,
    upload_file,
)

SCRIPT_PATH = str(Path(__file__).parent / "upload_to_mowen.py")


# --- File type detection ---


class TestDetectFileType:
    def test_image_extensions(self):
        assert detect_filetype("photo.png") == 1
        assert detect_filetype("photo.jpg") == 1
        assert detect_filetype("photo.jpeg") == 1
        assert detect_filetype("anim.gif") == 1
        assert detect_filetype("photo.webp") == 1

    def test_audio_extensions(self):
        assert detect_filetype("song.mp3") == 2
        assert detect_filetype("voice.m4a") == 2

    def test_pdf_extension(self):
        assert detect_filetype("doc.pdf") == 3

    def test_unknown_extension(self):
        assert detect_filetype("data.csv") is None
        assert detect_filetype("archive.zip") is None

    def test_case_insensitive(self):
        assert detect_filetype("PHOTO.PNG") == 1
        assert detect_filetype("Doc.PDF") == 3


# --- Missing API key ---


class TestMissingApiKey:
    def test_exit_without_api_key(self, tmp_path):
        dummy = tmp_path / "test.png"
        dummy.write_bytes(b"\x89PNG")
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, str(dummy)],
            capture_output=True,
            text=True,
            env={"PATH": "/usr/bin:/bin"},  # no MOWEN_API_KEY
        )
        assert result.returncode == 1
        assert "MOWEN_API_KEY" in result.stderr


# --- Prepare API call ---


class TestPrepareApiCall:
    @patch("upload_to_mowen.requests.post")
    def test_correct_request(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "data": {
                "endpoint": "https://oss.example.com",
                "form": {"key": "abc", "policy": "xyz"},
            }
        }
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = prepare_upload("test-key", "photo.png", 1)

        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert call_kwargs.kwargs["json"] == {"fileType": 1, "fileName": "photo.png"}
        assert "Bearer test-key" in call_kwargs.kwargs["headers"]["Authorization"]
        assert result["endpoint"] == "https://oss.example.com"

    @patch("upload_to_mowen.requests.post")
    def test_unwraps_data_field(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "data": {
                "endpoint": "https://oss.example.com",
                "form": {"key": "abc"},
            }
        }
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = prepare_upload("key", "file.png", 1)
        # Should unwrap the `data` wrapper
        assert "form" in result
        assert result["form"]["key"] == "abc"

    @patch("upload_to_mowen.requests.post")
    def test_no_data_wrapper(self, mock_post):
        """When API returns result without `data` wrapper."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "endpoint": "https://oss.example.com",
            "form": {"key": "abc"},
        }
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = prepare_upload("key", "file.png", 1)
        assert result["endpoint"] == "https://oss.example.com"


# --- Extract endpoint ---


class TestExtractEndpoint:
    def test_top_level_endpoint(self):
        data = {"endpoint": "https://oss.example.com", "form": {}}
        assert extract_endpoint(data) == "https://oss.example.com"

    def test_top_level_host(self):
        data = {"host": "https://oss.example.com", "form": {}}
        assert extract_endpoint(data) == "https://oss.example.com"

    def test_inside_form_fallback(self):
        data = {"form": {"host": "https://oss.example.com"}}
        assert extract_endpoint(data) == "https://oss.example.com"

    def test_missing_endpoint_raises(self):
        with pytest.raises(ValueError, match="Cannot find upload endpoint"):
            extract_endpoint({"form": {}})


# --- Upload to OSS ---


class TestUploadToOss:
    @patch("upload_to_mowen.requests.post")
    def test_upload_sends_form_fields_and_file(self, mock_post):
        # First call: prepare endpoint
        prepare_resp = MagicMock()
        prepare_resp.json.return_value = {
            "data": {
                "endpoint": "https://oss.example.com/upload",
                "form": {
                    "key": "uploads/abc.png",
                    "policy": "eyJleH...",
                    "OSSAccessKeyId": "LTAI...",
                    "signature": "sig123",
                    "callback": "cb64...",
                },
            }
        }
        prepare_resp.raise_for_status = MagicMock()

        # Second call: OSS upload
        upload_resp = MagicMock()
        upload_resp.json.return_value = {"uuid": "uuid-123-456"}
        upload_resp.raise_for_status = MagicMock()

        mock_post.side_effect = [prepare_resp, upload_resp]

        # Create a real temp file
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"\x89PNG fake image data")
            temp_path = Path(f.name)

        try:
            result = upload_file("test-key", temp_path)
        finally:
            temp_path.unlink()

        assert result["uuid"] == "uuid-123-456"
        assert result["fileName"] == temp_path.name
        assert result["fileType"] == 1

        # Verify the OSS upload call
        oss_call = mock_post.call_args_list[1]
        assert oss_call.args[0] == "https://oss.example.com/upload"
        # files= should contain the form fields + file
        files_arg = oss_call.kwargs["files"]
        field_names = [name for name, _ in files_arg]
        assert "key" in field_names
        assert "policy" in field_names
        assert "signature" in field_names
        assert "file" in field_names

    @patch("upload_to_mowen.requests.post")
    def test_uuid_from_nested_data(self, mock_post):
        """UUID nested inside data.uuid."""
        prepare_resp = MagicMock()
        prepare_resp.json.return_value = {
            "data": {
                "endpoint": "https://oss.example.com",
                "form": {"key": "k"},
            }
        }
        prepare_resp.raise_for_status = MagicMock()

        upload_resp = MagicMock()
        upload_resp.json.return_value = {"data": {"uuid": "nested-uuid"}}
        upload_resp.raise_for_status = MagicMock()

        mock_post.side_effect = [prepare_resp, upload_resp]

        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(b"\xff\xd8\xff")
            temp_path = Path(f.name)

        try:
            result = upload_file("key", temp_path)
        finally:
            temp_path.unlink()

        assert result["uuid"] == "nested-uuid"

    @patch("upload_to_mowen.requests.post")
    def test_missing_uuid_raises(self, mock_post):
        """OSS response without UUID should raise ValueError."""
        prepare_resp = MagicMock()
        prepare_resp.json.return_value = {
            "data": {
                "endpoint": "https://oss.example.com",
                "form": {"key": "k"},
            }
        }
        prepare_resp.raise_for_status = MagicMock()

        upload_resp = MagicMock()
        upload_resp.json.return_value = {"status": "ok"}  # no uuid field
        upload_resp.raise_for_status = MagicMock()

        mock_post.side_effect = [prepare_resp, upload_resp]

        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"\x89PNG")
            temp_path = Path(f.name)

        try:
            with pytest.raises(ValueError, match="UUID not found"):
                upload_file("key", temp_path)
        finally:
            temp_path.unlink()

    def test_unsupported_extension(self, tmp_path):
        bad_file = tmp_path / "data.csv"
        bad_file.write_text("a,b,c")
        with pytest.raises(ValueError, match="Unsupported file extension"):
            upload_file("key", bad_file)


# --- Full upload flow (end-to-end with mocks) ---


class TestFullUploadFlow:
    @patch("upload_to_mowen.requests.post")
    def test_end_to_end(self, mock_post):
        prepare_resp = MagicMock()
        prepare_resp.json.return_value = {
            "data": {
                "host": "https://oss.example.com",
                "form": {"key": "uploads/img.png", "policy": "p", "signature": "s"},
            }
        }
        prepare_resp.raise_for_status = MagicMock()

        upload_resp = MagicMock()
        upload_resp.json.return_value = {"uuid": "final-uuid-789"}
        upload_resp.raise_for_status = MagicMock()

        mock_post.side_effect = [prepare_resp, upload_resp]

        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"PNG data")
            temp_path = Path(f.name)

        try:
            result = upload_file("my-api-key", temp_path)
        finally:
            temp_path.unlink()

        assert result == {
            "uuid": "final-uuid-789",
            "fileName": temp_path.name,
            "fileType": 1,
        }

        # Verify prepare was called with correct auth
        prep_call = mock_post.call_args_list[0]
        assert prep_call.kwargs["headers"]["Authorization"] == "Bearer my-api-key"
        assert prep_call.kwargs["json"]["fileType"] == 1


# --- Batch upload (CLI) ---


class TestBatchUpload:
    def test_one_fails_one_succeeds(self, tmp_path):
        """When uploading multiple files, a missing file should not block others."""
        good_file = tmp_path / "good.png"
        good_file.write_bytes(b"\x89PNG")
        bad_file = tmp_path / "missing.png"  # does not exist

        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, str(good_file), str(bad_file)],
            capture_output=True,
            text=True,
            env={
                "PATH": "/usr/bin:/bin",
                "MOWEN_API_KEY": "test-key",
                # Ensure Python can find the requests module
                "PYTHONPATH": subprocess.run(
                    [sys.executable, "-c", "import sys; print(':'.join(sys.path))"],
                    capture_output=True, text=True,
                ).stdout.strip(),
            },
            timeout=10,
        )

        # Should exit with code 1 due to the failed file
        assert result.returncode == 1
        assert "missing.png" in result.stderr

    def test_all_missing(self, tmp_path):
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, "/nonexistent/a.png", "/nonexistent/b.jpg"],
            capture_output=True,
            text=True,
            env={
                "PATH": "/usr/bin:/bin",
                "MOWEN_API_KEY": "test-key",
                "PYTHONPATH": subprocess.run(
                    [sys.executable, "-c", "import sys; print(':'.join(sys.path))"],
                    capture_output=True, text=True,
                ).stdout.strip(),
            },
            timeout=10,
        )
        assert result.returncode == 1
        assert "a.png" in result.stderr
        assert "b.jpg" in result.stderr


# --- Pretty output ---


class TestPrettyOutput:
    @patch("upload_to_mowen.requests.post")
    def test_pretty_flag(self, mock_post, tmp_path):
        prepare_resp = MagicMock()
        prepare_resp.json.return_value = {
            "data": {
                "endpoint": "https://oss.example.com",
                "form": {"key": "k"},
            }
        }
        prepare_resp.raise_for_status = MagicMock()

        upload_resp = MagicMock()
        upload_resp.json.return_value = {"uuid": "pretty-uuid"}
        upload_resp.raise_for_status = MagicMock()

        mock_post.side_effect = [prepare_resp, upload_resp]

        img = tmp_path / "cover.png"
        img.write_bytes(b"\x89PNG")

        # Run via subprocess to test --pretty flag
        # We need to mock at the subprocess level, so instead test via main()
        from upload_to_mowen import main

        with patch("sys.argv", ["upload_to_mowen.py", str(img), "--pretty"]), \
             patch.dict("os.environ", {"MOWEN_API_KEY": "key"}), \
             patch("sys.exit") as mock_exit, \
             patch("builtins.print") as mock_print:
            # Reset side_effect for fresh mocks
            mock_post.side_effect = [prepare_resp, upload_resp]
            main()

        # Verify pretty-printed output (indent=2)
        printed = mock_print.call_args_list[0][0][0]
        parsed = json.loads(printed)
        assert parsed["uuid"] == "pretty-uuid"
        # Pretty output should have newlines (indentation)
        assert "\n" in printed

    @patch("upload_to_mowen.requests.post")
    def test_compact_output(self, mock_post, tmp_path):
        prepare_resp = MagicMock()
        prepare_resp.json.return_value = {
            "data": {
                "endpoint": "https://oss.example.com",
                "form": {"key": "k"},
            }
        }
        prepare_resp.raise_for_status = MagicMock()

        upload_resp = MagicMock()
        upload_resp.json.return_value = {"uuid": "compact-uuid"}
        upload_resp.raise_for_status = MagicMock()

        mock_post.side_effect = [prepare_resp, upload_resp]

        img = tmp_path / "cover.png"
        img.write_bytes(b"\x89PNG")

        from upload_to_mowen import main

        with patch("sys.argv", ["upload_to_mowen.py", str(img)]), \
             patch.dict("os.environ", {"MOWEN_API_KEY": "key"}), \
             patch("sys.exit") as mock_exit, \
             patch("builtins.print") as mock_print:
            mock_post.side_effect = [prepare_resp, upload_resp]
            main()

        printed = mock_print.call_args_list[0][0][0]
        # Compact output should be a single line
        assert "\n" not in printed
        parsed = json.loads(printed)
        assert parsed["uuid"] == "compact-uuid"
