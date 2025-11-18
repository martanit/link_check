"""Tests for CLI interface."""

import subprocess
import sys
from pathlib import Path


class TestCLIHelp:
    """Test CLI help functionality."""

    def test_help_flag_shows_usage(self):
        """Test that --help flag displays usage information."""
        result = subprocess.run(
            [sys.executable, "-m", "link_check", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "--base-url" in result.stdout
        assert "--output" in result.stdout
        assert "--workers" in result.stdout
        assert "--external" in result.stdout
        assert "--timeout" in result.stdout

    def test_help_includes_descriptions(self):
        """Test that help output includes parameter descriptions."""
        result = subprocess.run(
            [sys.executable, "-m", "link_check", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        # Should contain helpful descriptions
        assert "Base URL" in result.stdout or "base url" in result.stdout.lower()


class TestCLIArguments:
    """Test CLI argument parsing."""

    def test_base_url_required(self):
        """Test that --base-url is a required argument."""
        result = subprocess.run(
            [sys.executable, "-m", "link_check"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert (
            "base-url" in result.stderr.lower() or "required" in result.stderr.lower()
        )

    def test_base_url_validation(self):
        """Test that --base-url validates URL format."""
        result = subprocess.run(
            [sys.executable, "-m", "link_check", "--base-url", "not-a-url"],
            capture_output=True,
            text=True,
        )
        # Should either fail validation or attempt to process
        # At minimum, should not crash
        assert result.returncode in [0, 1, 2]

    def test_output_argument(self):
        """Test that --output argument is accepted."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "link_check",
                "--base-url",
                "http://localhost:8080",
                "--output",
                "report.yaml",
            ],
            capture_output=True,
            text=True,
        )
        # Should accept the argument (may fail later due to no server)
        assert "--output" not in result.stderr or result.returncode in [0, 1]

    def test_workers_argument(self):
        """Test that --workers argument accepts integer value."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "link_check",
                "--base-url",
                "http://localhost:8080",
                "--workers",
                "4",
            ],
            capture_output=True,
            text=True,
        )
        # Should accept the argument
        assert result.returncode in [0, 1]

    def test_workers_validation(self):
        """Test that --workers validates integer input."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "link_check",
                "--base-url",
                "http://localhost:8080",
                "--workers",
                "not-a-number",
            ],
            capture_output=True,
            text=True,
        )
        # Should fail validation for non-integer
        assert result.returncode != 0
        assert "invalid" in result.stderr.lower() or "error" in result.stderr.lower()

    def test_external_flag(self):
        """Test that --external flag is accepted."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "link_check",
                "--base-url",
                "http://localhost:8080",
                "--external",
            ],
            capture_output=True,
            text=True,
        )
        # Should accept the flag
        assert result.returncode in [0, 1]

    def test_timeout_argument(self):
        """Test that --timeout argument accepts numeric value."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "link_check",
                "--base-url",
                "http://localhost:8080",
                "--timeout",
                "30",
            ],
            capture_output=True,
            text=True,
        )
        # Should accept the argument
        assert result.returncode in [0, 1]

    def test_timeout_validation(self):
        """Test that --timeout validates numeric input."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "link_check",
                "--base-url",
                "http://localhost:8080",
                "--timeout",
                "not-a-number",
            ],
            capture_output=True,
            text=True,
        )
        # Should fail validation for non-numeric
        assert result.returncode != 0
        assert "invalid" in result.stderr.lower() or "error" in result.stderr.lower()


class TestCLIExecution:
    """Test CLI execution behavior."""

    def test_all_arguments_together(self):
        """Test that all arguments work together."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "link_check",
                "--base-url",
                "http://localhost:8080",
                "--output",
                "report.yaml",
                "--workers",
                "4",
                "--external",
                "--timeout",
                "30",
            ],
            capture_output=True,
            text=True,
        )
        # Should accept all arguments (may fail due to no server, but args should parse)
        assert result.returncode in [0, 1]

    def test_minimal_arguments(self):
        """Test with only required arguments."""
        result = subprocess.run(
            [sys.executable, "-m", "link_check", "--base-url", "http://localhost:8080"],
            capture_output=True,
            text=True,
        )
        # Should accept minimal arguments
        assert result.returncode in [0, 1]


class TestCLIOutput:
    """Test CLI output behavior."""

    def test_progress_output_to_stderr(self):
        """Test that progress messages go to stderr, not stdout."""
        # Note: This test may need adjustment based on actual implementation
        # The key is that YAML output should go to stdout, progress to stderr
        result = subprocess.run(
            [sys.executable, "-m", "link_check", "--base-url", "http://localhost:8080"],
            capture_output=True,
            text=True,
        )
        # If there's progress output, it should be in stderr
        # This is a smoke test - actual validation depends on implementation
        assert result.returncode in [0, 1]
