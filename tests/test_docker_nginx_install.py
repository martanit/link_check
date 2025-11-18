"""
Test suite for Task 1.2: Install nginx in Docker Image

This test verifies that nginx is properly installed in the Docker image.

According to CLAUDE.md test integrity rules:
- Tests define expected behavior
- If tests fail, the implementation is wrong, not the test
- Tests should only be changed if provably broken
"""

import subprocess
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


@pytest.fixture(scope="module")
def docker_image():
    """Build the Docker image before running tests."""
    image_name = "mkdocs-nginx:test"

    # Build the image
    result = subprocess.run(
        ["docker", "build", "-f", "docker/Dockerfile", "-t", image_name, "."],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        pytest.fail(f"Docker image build failed:\n{result.stderr}")

    yield image_name

    # Cleanup is optional - we can leave the test image for manual inspection


def run_docker_command(image, command):
    """Helper function to run a command in the Docker container."""
    result = subprocess.run(
        ["docker", "run", "--rm", image] + command, capture_output=True, text=True
    )
    return result


class TestNginxInstallation:
    """Test suite for nginx installation in Docker image."""

    def test_nginx_version_command(self, docker_image):
        """Test that nginx -v shows version information."""
        result = run_docker_command(docker_image, ["nginx", "-v"])

        # nginx outputs version to stderr, not stdout
        assert result.returncode == 0, "nginx -v command should succeed"
        assert (
            "nginx version" in result.stderr.lower()
        ), "nginx version output should contain 'nginx version'"

    def test_nginx_binary_in_path(self, docker_image):
        """Test that nginx binary is in PATH."""
        result = run_docker_command(docker_image, ["which", "nginx"])

        assert result.returncode == 0, "which nginx should find the binary"
        assert "/nginx" in result.stdout, "nginx should be in a bin directory"
        assert result.stdout.strip() != "", "which should return a non-empty path"

    def test_nginx_binary_executable(self, docker_image):
        """Test that nginx binary has executable permissions."""
        result = run_docker_command(
            docker_image, ["sh", "-c", "[ -x $(which nginx) ] && echo 'executable'"]
        )

        assert result.returncode == 0, "nginx binary should be executable"
        assert "executable" in result.stdout, "nginx should have execute permissions"

    def test_nginx_help_command(self, docker_image):
        """Test that nginx -h shows help information."""
        result = run_docker_command(docker_image, ["nginx", "-h"])

        # nginx help might exit with 0 or 1 depending on version
        assert (
            "Usage: nginx" in result.stderr or "usage: nginx" in result.stderr.lower()
        ), "nginx help should show usage information"

    def test_nginx_test_config(self, docker_image):
        """Test that nginx -t can test configuration (even if config missing)."""
        result = run_docker_command(docker_image, ["nginx", "-t"])

        # This might fail because config doesn't exist yet, but the nginx
        # binary should be functional enough to attempt the test
        # We're just checking the binary works, not that config exists
        assert (
            "nginx" in result.stderr.lower()
        ), "nginx -t should produce nginx-related output"


class TestAcceptanceCriteria:
    """Tests directly from the acceptance criteria in issue #6."""

    def test_acceptance_build_image(self, docker_image):
        """Acceptance: docker build -f docker/Dockerfile -t mkdocs-nginx:test ."""
        # This is tested by the fixture, but we verify the image exists
        result = subprocess.run(
            ["docker", "images", docker_image, "--format", "{{.Repository}}:{{.Tag}}"],
            capture_output=True,
            text=True,
        )

        assert docker_image in result.stdout, f"Image {docker_image} should exist"

    def test_acceptance_nginx_version(self, docker_image):
        """Acceptance: docker run --rm mkdocs-nginx:test nginx -v"""
        result = run_docker_command(docker_image, ["nginx", "-v"])

        assert result.returncode == 0, "Acceptance criteria: nginx -v should succeed"

    def test_acceptance_which_nginx(self, docker_image):
        """Acceptance: docker run --rm mkdocs-nginx:test which nginx"""
        result = run_docker_command(docker_image, ["which", "nginx"])

        assert result.returncode == 0, "Acceptance criteria: which nginx should succeed"
        assert (
            result.stdout.strip() != ""
        ), "Acceptance criteria: which nginx should return a path"
