"""Run research paper platform tests."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from test_arxiv import test_arxiv_papers
from test_semanticscholar import test_semanticscholar_papers
from test_openreview import test_openreview_papers


async def run_paper_tests():
    """Run all research paper platform tests sequentially."""

    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + " " * 10 + "RESEARCH PAPER PLATFORMS TEST SUITE" + " " * 23 + "█")
    print("█" * 68 + "█")
    print("█" * 70)
    print("\n")

    tests_passed = 0
    tests_failed = 0

    # Test 1: arXiv
    print("\n📄 Running arXiv Tests...\n")
    try:
        await test_arxiv_papers()
        tests_passed += 1
        print("\n✅ arXiv Tests: PASSED\n")
    except Exception as e:
        tests_failed += 1
        print(f"\n❌ arXiv Tests: FAILED - {e}\n")

    print("\n" + "─" * 70 + "\n")

    # Test 2: Semantic Scholar
    print("\n🎓 Running Semantic Scholar Tests...\n")
    try:
        await test_semanticscholar_papers()
        tests_passed += 1
        print("\n✅ Semantic Scholar Tests: PASSED\n")
    except Exception as e:
        tests_failed += 1
        print(f"\n❌ Semantic Scholar Tests: FAILED - {e}\n")

    print("\n" + "─" * 70 + "\n")

    # Test 3: OpenReview
    print("\n🏆 Running OpenReview Tests...\n")
    try:
        await test_openreview_papers()
        tests_passed += 1
        print("\n✅ OpenReview Tests: PASSED\n")
    except Exception as e:
        tests_failed += 1
        print(f"\n❌ OpenReview Tests: FAILED - {e}\n")

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
    print("  Note: Tests require internet connection to access APIs.")
    print("        Rate limits may affect test results.")
    print()
    print("█" * 70)
    print()

    return tests_failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_paper_tests())
    sys.exit(0 if success else 1)
