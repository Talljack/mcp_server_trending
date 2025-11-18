"""Run all new feature tests."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from test_pypi import test_pypi_trending
from test_wordpress import test_wordpress_plugins
from test_remoteok import test_remoteok_jobs
from test_aggregation import test_aggregation_analysis


async def run_all_tests():
    """Run all new feature tests sequentially."""

    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + " " * 15 + "NEW FEATURES TEST SUITE" + " " * 30 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    print("\n")

    tests_passed = 0
    tests_failed = 0

    # Test 1: PyPI
    print("\n📦 Running PyPI Tests...\n")
    try:
        await test_pypi_trending()
        tests_passed += 1
        print("\n✅ PyPI Tests: PASSED\n")
    except Exception as e:
        tests_failed += 1
        print(f"\n❌ PyPI Tests: FAILED - {e}\n")

    print("\n" + "─" * 70 + "\n")

    # Test 2: WordPress
    print("\n🔌 Running WordPress Tests...\n")
    try:
        await test_wordpress_plugins()
        tests_passed += 1
        print("\n✅ WordPress Tests: PASSED\n")
    except Exception as e:
        tests_failed += 1
        print(f"\n❌ WordPress Tests: FAILED - {e}\n")

    print("\n" + "─" * 70 + "\n")

    # Test 3: RemoteOK
    print("\n💼 Running RemoteOK Tests...\n")
    try:
        await test_remoteok_jobs()
        tests_passed += 1
        print("\n✅ RemoteOK Tests: PASSED\n")
    except Exception as e:
        tests_failed += 1
        print(f"\n❌ RemoteOK Tests: FAILED - {e}\n")

    print("\n" + "─" * 70 + "\n")

    # Test 4: Aggregation
    print("\n🔬 Running Aggregation Analysis Tests...\n")
    try:
        await test_aggregation_analysis()
        tests_passed += 1
        print("\n✅ Aggregation Tests: PASSED\n")
    except Exception as e:
        tests_failed += 1
        print(f"\n❌ Aggregation Tests: FAILED - {e}\n")

    # Summary
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + " " * 25 + "TEST SUMMARY" + " " * 31 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    print()

    total_tests = tests_passed + tests_failed
    pass_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0

    print(f"  Total Test Suites: {total_tests}")
    print(f"  Passed: {tests_passed} ✅")
    print(f"  Failed: {tests_failed} ❌")
    print(f"  Pass Rate: {pass_rate:.1f}%")
    print()

    if tests_failed == 0:
        print("  🎉 ALL TESTS PASSED!")
    elif tests_passed >= tests_failed:
        print("  ⚠️  SOME TESTS FAILED (but most passed)")
    else:
        print("  ❌ MAJORITY OF TESTS FAILED")

    print()
    print("  Note: RemoteOK tests may fail in VPN/proxy environments.")
    print("        This is expected behavior - the code is correct.")
    print()
    print("█" * 70)
    print()

    return tests_failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
