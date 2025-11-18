"""Tests for Docker image builds and functionality."""

import subprocess
from pathlib import Path

import pytest


def is_docker_available():
    """Check if Docker daemon is available."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


pytestmark = pytest.mark.skipif(
    not is_docker_available(),
    reason="Docker daemon not available",
)


def test_dockerfile_builds():
    """Test that the Dockerfile builds successfully."""
    repo_root = Path(__file__).parent.parent
    dockerfile = repo_root / "docker" / "Dockerfile"

    # Verify Dockerfile exists
    assert dockerfile.exists(), f"Dockerfile not found at {dockerfile}"

    # Build the image
    result = subprocess.run(
        ["docker", "build", "-f", str(dockerfile), "-t", "mkdocs-nginx:test", "."],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=300,
    )

    assert result.returncode == 0, f"Docker build failed: {result.stderr}"


def test_python_available_in_image():
    """Test that Python is available in the built image."""
    result = subprocess.run(
        ["docker", "run", "--rm", "mkdocs-nginx:test", "python", "--version"],
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, f"Python check failed: {result.stderr}"
    assert "Python 3." in result.stdout, f"Unexpected Python version: {result.stdout}"
