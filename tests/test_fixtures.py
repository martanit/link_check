"""Tests for test fixtures to ensure they build correctly."""

import subprocess
from pathlib import Path


def test_minimal_mkdocs_fixture_builds():
    """Test that the minimal MkDocs fixture builds successfully."""
    fixture_path = Path(__file__).parent / "fixtures" / "minimal-mkdocs"
    result = subprocess.run(
        ["uv", "run", "mkdocs", "build", "--strict"],
        cwd=fixture_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"Build failed: {result.stderr}"

    # Verify output files exist
    site_dir = fixture_path / "site"
    assert (site_dir / "index.html").exists()
    assert (site_dir / "page1" / "index.html").exists()
    assert (site_dir / "page2" / "index.html").exists()


def test_monorepo_fixture_builds():
    """Test that the monorepo fixture builds successfully."""
    fixture_path = Path(__file__).parent / "fixtures" / "monorepo-mkdocs"
    result = subprocess.run(
        ["uv", "run", "mkdocs", "build", "--strict"],
        cwd=fixture_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"Build failed: {result.stderr}"

    # Verify output files exist (monorepo only uses subsites, no root index)
    site_dir = fixture_path / "site"
    assert (site_dir / "subsite-1" / "index.html").exists()
    assert (site_dir / "subsite-2" / "index.html").exists()
    assert (site_dir / "subsite-1" / "features" / "index.html").exists()
    assert (site_dir / "subsite-2" / "guide" / "index.html").exists()


def test_monorepo_fixture_structure():
    """Test that the monorepo fixture has correct directory structure."""
    fixture_path = Path(__file__).parent / "fixtures" / "monorepo-mkdocs"

    # Check source files (no root docs, only subsites)
    assert (fixture_path / "mkdocs.yml").exists()
    assert (fixture_path / "subsite1" / "mkdocs.yml").exists()
    assert (fixture_path / "subsite1" / "docs" / "index.md").exists()
    assert (fixture_path / "subsite1" / "docs" / "features.md").exists()
    assert (fixture_path / "subsite2" / "mkdocs.yml").exists()
    assert (fixture_path / "subsite2" / "docs" / "index.md").exists()
    assert (fixture_path / "subsite2" / "docs" / "guide.md").exists()
