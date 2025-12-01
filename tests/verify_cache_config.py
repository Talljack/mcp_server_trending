"""验证论文平台缓存配置"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.server import TrendingMCPServer


def verify_cache_ttl():
    """验证各个 fetcher 的缓存时间配置"""

    print("=" * 60)
    print("验证论文平台缓存配置")
    print("=" * 60)
    print()

    server = TrendingMCPServer()

    # 检查各个 fetcher 的缓存时间
    fetchers = [
        ("arXiv", server.arxiv_fetcher, 86400, "24小时"),
        ("Semantic Scholar", server.semanticscholar_fetcher, 86400, "24小时"),
        ("OpenReview", server.openreview_fetcher, 86400, "24小时"),
        ("GitHub", server.github_fetcher, 3600, "1小时"),
        ("Hacker News", server.hackernews_fetcher, 3600, "1小时"),
    ]

    print("缓存时间配置：")
    print("-" * 60)

    all_correct = True
    for name, fetcher, expected_ttl, description in fetchers:
        actual_ttl = fetcher.cache_ttl
        status = "✅" if actual_ttl == expected_ttl else "❌"
        print(
            f"{status} {name:20s}: {actual_ttl:7d}秒 ({description}) - {'正确' if actual_ttl == expected_ttl else f'期望 {expected_ttl}'}"
        )

        if actual_ttl != expected_ttl:
            all_correct = False

    print()
    print("=" * 60)

    if all_correct:
        print("✅ 所有缓存配置正确！")
        print()
        print("论文平台优化：")
        print("  - 所有论文平台统一使用 24小时缓存")
        print("  - arXiv: 24小时（相比默认提升 24倍）")
        print("  - Semantic Scholar: 24小时（相比默认提升 24倍）")
        print("  - OpenReview: 24小时（相比默认提升 24倍）")
        print()
        print("预计效果：减少 95%+ 的 API 调用 🎉")
    else:
        print("❌ 部分配置不正确，请检查")

    print("=" * 60)


if __name__ == "__main__":
    verify_cache_ttl()
