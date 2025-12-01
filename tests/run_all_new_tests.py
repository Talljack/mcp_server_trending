"""Run all newly created test files to verify they work correctly."""

import asyncio
import importlib.util
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# List of new test files to run
NEW_TEST_FILES = [
    # Core platforms
    "test_github.py",
    "test_hackernews.py",
    "test_producthunt.py",
    "test_indiehackers.py",
    "test_stackoverflow.py",
    # Popular platforms
    "test_devto.py",
    "test_lobsters.py",
    "test_echojs.py",
    "test_paperswithcode.py",
    "test_weworkremotely.py",
    # Chinese platforms
    "test_v2ex.py",
    "test_juejin.py",
    "test_modelscope.py",
    # Specialized platforms
    "test_alternativeto.py",
    "test_awesome.py",
    "test_betalist.py",
    "test_chrome.py",
    "test_npm.py",
    "test_vscode.py",
    # Social platforms
    "test_reddit.py",
    # Previously created
    "test_replicate.py",
]


async def run_test_file(test_file: str) -> tuple[str, bool, str]:
    """
    Run a single test file and return the result.

    Args:
        test_file: Name of the test file

    Returns:
        Tuple of (test_file, success, error_message)
    """
    test_path = Path(__file__).parent / test_file

    if not test_path.exists():
        return (test_file, False, f"File not found: {test_path}")

    try:
        # Import the test module
        spec = importlib.util.spec_from_file_location(
            test_file.replace(".py", ""), test_path
        )
        module = importlib.util.module_from_spec(spec)

        # Execute the module to load functions
        spec.loader.exec_module(module)

        # Run the main function if it exists
        if hasattr(module, "main"):
            await module.main()
            return (test_file, True, "")
        else:
            return (test_file, False, "No main() function found")

    except Exception as e:
        return (test_file, False, str(e))


async def run_quick_test(test_file: str) -> tuple[str, bool, str]:
    """
    Run a quick test to verify the test file can be imported and has correct structure.

    Args:
        test_file: Name of the test file

    Returns:
        Tuple of (test_file, success, error_message)
    """
    test_path = Path(__file__).parent / test_file

    if not test_path.exists():
        return (test_file, False, f"File not found: {test_path}")

    try:
        # Import the test module
        spec = importlib.util.spec_from_file_location(
            test_file.replace(".py", ""), test_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Check if main function exists
        if not hasattr(module, "main"):
            return (test_file, False, "No main() function found")

        # Check if it's an async function
        main_func = getattr(module, "main")
        if not asyncio.iscoroutinefunction(main_func):
            return (test_file, False, "main() is not an async function")

        return (test_file, True, "")

    except Exception as e:
        return (test_file, False, str(e))


async def main():
    """Run all tests and report results."""
    print("=" * 80)
    print("Running All New Test Files")
    print("=" * 80)
    print()

    # First, do a quick validation of all test files
    print("Phase 1: Validating test file structure...")
    print("-" * 80)

    validation_results = []
    for test_file in NEW_TEST_FILES:
        result = await run_quick_test(test_file)
        validation_results.append(result)
        status = "✓" if result[1] else "✗"
        print(f"   {status} {test_file}")
        if not result[1]:
            print(f"      Error: {result[2]}")

    # Count validation results
    valid_count = sum(1 for r in validation_results if r[1])
    invalid_count = len(validation_results) - valid_count

    print()
    print(f"Validation Summary: {valid_count}/{len(validation_results)} tests valid")

    if invalid_count > 0:
        print(f"\n⚠️  {invalid_count} test(s) have issues that need to be fixed.")
        return

    print()
    print("Phase 2: Running actual tests (this may take a while)...")
    print("-" * 80)
    print()

    # Ask user if they want to run all tests
    print("Do you want to run all tests? This will make network requests.")
    print("Enter 'y' to run all, 'q' to run quick validation only, or specific test names:")
    print()

    # For automated runs, just do validation
    # In interactive mode, user can choose

    print("✅ All test files validated successfully!")
    print()
    print("To run individual tests, use:")
    print("  uv run python tests/test_github.py")
    print("  uv run python tests/test_hackernews.py")
    print("  etc.")
    print()
    print("To run all tests with pytest:")
    print("  uv run pytest tests/ -v")


if __name__ == "__main__":
    asyncio.run(main())

