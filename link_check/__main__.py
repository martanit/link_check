"""CLI interface for link checker."""

import argparse
import sys
from typing import Optional


def validate_url(url: str) -> str:
    """Validate URL format.

    Args:
        url: URL string to validate

    Returns:
        The validated URL

    Raises:
        argparse.ArgumentTypeError: If URL format is invalid
    """
    if not url:
        raise argparse.ArgumentTypeError("URL cannot be empty")

    # Basic URL validation - check for scheme
    if not (url.startswith("http://") or url.startswith("https://")):
        # Allow it but warn - this is lenient validation
        pass

    return url


def validate_positive_int(value: str) -> int:
    """Validate positive integer.

    Args:
        value: String to parse as integer

    Returns:
        The validated integer

    Raises:
        argparse.ArgumentTypeError: If value is not a positive integer
    """
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer")


def validate_positive_number(value: str) -> float:
    """Validate positive number.

    Args:
        value: String to parse as number

    Returns:
        The validated number

    Raises:
        argparse.ArgumentTypeError: If value is not a positive number
    """
    try:
        fvalue = float(value)
        if fvalue <= 0:
            raise argparse.ArgumentTypeError(f"{value} is not a positive number")
        return fvalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid number")


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: List of argument strings (for testing), None to use sys.argv

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Check links in HTML documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check links with default settings
  python -m link_check --base-url http://localhost:8080

  # Check with all options
  python -m link_check --base-url http://localhost:8080 \\
      --output report.yaml --workers 4 --external --timeout 30
        """,
    )

    parser.add_argument(
        "--base-url",
        required=True,
        type=validate_url,
        help="Base URL to check (e.g., http://localhost:8080)",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path for YAML report (default: stdout)",
    )

    parser.add_argument(
        "--workers",
        type=validate_positive_int,
        default=4,
        help="Number of parallel workers (default: 4)",
    )

    parser.add_argument(
        "--external",
        action="store_true",
        default=False,
        help="Check external links (default: False)",
    )

    parser.add_argument(
        "--timeout",
        type=validate_positive_number,
        default=10.0,
        help="HTTP timeout in seconds (default: 10)",
    )

    return parser.parse_args(args)


def main() -> int:
    """Main entry point for CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        args = parse_args()

        # Progress output goes to stderr
        print(f"Starting link checker...", file=sys.stderr)
        print(f"Base URL: {args.base_url}", file=sys.stderr)
        print(f"Workers: {args.workers}", file=sys.stderr)
        print(f"Timeout: {args.timeout}s", file=sys.stderr)
        print(f"Check external links: {args.external}", file=sys.stderr)

        if args.output:
            print(f"Output: {args.output}", file=sys.stderr)
        else:
            print(f"Output: stdout", file=sys.stderr)

        # TODO: Implement actual link checking logic
        # For now, this is a skeleton that accepts all arguments
        print("Link checking not yet implemented", file=sys.stderr)

        # Output minimal YAML to stdout if no output file specified
        if not args.output:
            print("summary:")
            print("  total_pages: 0")
            print("  total_links: 0")
            print("  broken_links: 0")
            print("broken_links: []")

        return 0

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
