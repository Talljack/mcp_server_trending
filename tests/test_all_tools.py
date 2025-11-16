"""测试所有 MCP Tools 是否正常调用"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_trending.server import TrendingMCPServer


async def test_all_tools():
    """测试所有 MCP tools"""
    print("=" * 70)
    print("测试所有 MCP Server Tools")
    print("=" * 70)

    server = TrendingMCPServer()

    # 测试配置 - 直接调用 fetcher 方法
    tests = [
        # GitHub Tools
        {
            "name": "get_github_trending_repos",
            "fetcher": server.github_fetcher,
            "method": "fetch_trending_repositories",
            "kwargs": {"language": "python", "time_range": "daily"},
            "description": "GitHub Trending 仓库",
        },
        # Hacker News Tools
        {
            "name": "get_hackernews_stories",
            "fetcher": server.hackernews_fetcher,
            "method": "fetch_stories",
            "kwargs": {"story_type": "top", "limit": 3},
            "description": "Hacker News 热门故事",
        },
        # Product Hunt Tools
        {
            "name": "get_producthunt_products",
            "fetcher": server.producthunt_fetcher,
            "method": "fetch_products",
            "kwargs": {"time_range": "today"},
            "description": "Product Hunt 产品",
        },
        # Indie Hackers Tools
        {
            "name": "get_indiehackers_popular",
            "fetcher": server.indiehackers_fetcher,
            "method": "fetch_popular_posts",
            "kwargs": {"limit": 3},
            "description": "Indie Hackers 热门讨论",
        },
        {
            "name": "get_indiehackers_income_reports",
            "fetcher": server.indiehackers_fetcher,
            "method": "fetch_income_reports",
            "kwargs": {"limit": 3},
            "description": "Indie Hackers 收入报告",
        },
        # Reddit Tools - Disabled: Requires API credentials
        # {
        #     "name": "get_reddit_trending",
        #     "fetcher": server.reddit_fetcher,
        #     "method": "fetch_trending",
        #     "kwargs": {"subreddit": "programming", "limit": 3},
        #     "description": "Reddit 热门帖子",
        # },
        # OpenRouter Tools (需要 API key)
        {
            "name": "get_openrouter_models",
            "fetcher": server.openrouter_fetcher,
            "method": "fetch_models",
            "kwargs": {"limit": 3},
            "description": "OpenRouter LLM 模型列表",
            "requires_api_key": True,
        },
        # TrustMRR Tools (新增)
        {
            "name": "get_trustmrr_rankings",
            "fetcher": server.trustmrr_fetcher,
            "method": "fetch_rankings",
            "kwargs": {"limit": 5},
            "description": "TrustMRR MRR 排行榜",
        },
        # AI Tools Directory (新增)
        {
            "name": "get_ai_tools",
            "fetcher": server.aitools_fetcher,
            "method": "fetch_trending",
            "kwargs": {"limit": 5},
            "description": "AI Tools Directory 热门工具",
        },
    ]

    results = {"success": [], "failed": [], "skipped": []}

    for i, test in enumerate(tests, 1):
        tool_name = test["name"]
        fetcher = test["fetcher"]
        method_name = test["method"]
        kwargs = test["kwargs"]
        desc = test["description"]
        requires_api_key = test.get("requires_api_key", False)

        print(f"\n[{i}/{len(tests)}] 测试: {desc} ({tool_name})")
        print("-" * 70)

        try:
            # 获取并调用方法
            method = getattr(fetcher, method_name)
            response = await method(**kwargs)

            # 检查响应
            if response.success:
                count = len(response.data)
                print(f"✅ 成功获取 {count} 条数据")

                # 显示第一条数据的摘要
                if count > 0:
                    first_item = response.data[0]
                    if hasattr(first_item, "name"):
                        print(f"   示例: {first_item.name}")
                    elif hasattr(first_item, "title"):
                        print(f"   示例: {first_item.title}")
                    elif hasattr(first_item, "content"):
                        content_preview = first_item.content[:50] if first_item.content else ""
                        print(f"   示例: {content_preview}...")

                results["success"].append(tool_name)
            else:
                # 检查是否是预期的 API key 错误
                if requires_api_key and response.error and "API key" in response.error:
                    print("⚠️  需要配置 API Key (预期行为)")
                    print("   获取地址: https://openrouter.ai/keys")
                    results["skipped"].append(tool_name)
                else:
                    print("❌ 调用失败")
                    error_preview = str(response.error)[:200] if response.error else "未知错误"
                    print(f"   错误: {error_preview}")
                    results["failed"].append(tool_name)

        except Exception as e:
            print(f"❌ 异常: {str(e)}")
            import traceback

            traceback.print_exc()
            results["failed"].append(tool_name)

    # 汇总结果
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)

    print(f"\n✅ 成功: {len(results['success'])} 个")
    for tool in results["success"]:
        print(f"   - {tool}")

    if results["skipped"]:
        print(f"\n⚠️  跳过 (需要 API Key): {len(results['skipped'])} 个")
        for tool in results["skipped"]:
            print(f"   - {tool}")

    if results["failed"]:
        print(f"\n❌ 失败: {len(results['failed'])} 个")
        for tool in results["failed"]:
            print(f"   - {tool}")

    # 清理
    await server.cleanup()

    # 返回测试结果
    total_tests = len(tests)
    actual_tests = total_tests - len(results["skipped"])
    passed_tests = len(results["success"])

    print(f"\n总计: {passed_tests}/{actual_tests} 个测试通过")

    if results["failed"]:
        print("\n⚠️  部分测试失败，请检查网络连接或 API 配置")
        return False
    else:
        print("\n🎉 所有测试通过！")
        return True


if __name__ == "__main__":
    success = asyncio.run(test_all_tools())
    sys.exit(0 if success else 1)
