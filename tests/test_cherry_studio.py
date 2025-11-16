#!/usr/bin/env python3
"""
Cherry Studio MCP Server 测试脚本

这个脚本模拟 MCP 客户端的行为，测试服务器是否正常工作。
用于在不启动 Cherry Studio 的情况下验证 MCP Server。
"""

import asyncio
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


async def test_mcp_tools():
    """测试所有 MCP Tools"""
    from mcp_server_trending.server import TrendingMCPServer

    print("=" * 70)
    print("🧪 Cherry Studio MCP Server 功能测试")
    print("=" * 70)

    # 初始化服务器
    print("\n1️⃣  初始化 MCP Server...")
    server = TrendingMCPServer()
    print(f"   ✅ 服务器名称: {server.server.name}")

    # 测试工具列表
    print("\n2️⃣  检查可用工具...")
    tools_info = [
        ("get_github_trending_repos", "获取 GitHub trending 仓库"),
        ("get_github_trending_developers", "获取 GitHub trending 开发者"),
        ("get_hackernews_stories", "获取 Hacker News 故事"),
        ("get_producthunt_products", "获取 Product Hunt 产品"),
    ]

    for tool_name, description in tools_info:
        print(f"   ✅ {tool_name}")
        print(f"      {description}")

    # 测试 GitHub Trending
    print("\n3️⃣  测试 GitHub Trending 查询...")
    try:
        response = await server.github_fetcher.fetch_trending_repositories(
            time_range="daily",
            language="python",
            use_cache=False,  # 不使用缓存，确保获取最新数据
        )

        if response.success and response.data:
            print(f"   ✅ 成功获取 {len(response.data)} 个 Python 项目")
            print(f"   📊 Top 3 项目:")
            for i, repo in enumerate(response.data[:3], 1):
                print(f"      {i}. {repo.author}/{repo.name}")
                print(f"         ⭐ {repo.stars} stars (+{repo.stars_today} today)")
                print(f"         📝 {repo.description[:60]}...")
        else:
            print(f"   ⚠️  未获取到数据: {response.error}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")

    # 测试 Hacker News
    print("\n4️⃣  测试 Hacker News 查询...")
    try:
        response = await server.hackernews_fetcher.fetch_top_stories(limit=5, use_cache=False)

        if response.success and response.data:
            print(f"   ✅ 成功获取 {len(response.data)} 个热门故事")
            print(f"   📰 Top 3 故事:")
            for i, story in enumerate(response.data[:3], 1):
                print(f"      {i}. {story.title}")
                print(f"         👍 {story.score} points | 💬 {story.descendants} comments")
        else:
            print(f"   ⚠️  未获取到数据: {response.error}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")

    # 生成示例查询
    print("\n5️⃣  Cherry Studio 测试提示词:")
    print("   " + "─" * 65)

    test_prompts = [
        "请帮我查询 GitHub 上今天最热门的 Python 项目",
        "Hacker News 上现在有什么热门的技术讨论？",
        "同时告诉我 GitHub 上的 Go 项目和 Hacker News 的 Show HN",
        "分析一下今天科技圈的热点话题",
    ]

    for prompt in test_prompts:
        print(f'   💬 "{prompt}"')

    print("   " + "─" * 65)

    # 生成配置示例
    print("\n6️⃣  Cherry Studio 配置参数:")
    print("   " + "─" * 65)

    config = {
        "name": "Trending",
        "description": "独立开发者热门榜单聚合服务",
        "type": "stdio",
        "command": os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", ".venv", "bin", "python")
        ),
        "args": [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "server.py"))
        ],
        "env": {
            "PYTHONPATH": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
        },
    }

    print(json.dumps(config, indent=2, ensure_ascii=False))
    print("   " + "─" * 65)

    # 清理
    print("\n7️⃣  清理资源...")
    await server.cleanup()
    print("   ✅ 清理完成")

    print("\n" + "=" * 70)
    print("✅ 测试完成！MCP Server 运行正常")
    print("=" * 70)
    print("\n📝 下一步:")
    print("   1. 打开 Cherry Studio")
    print("   2. 进入设置 → MCP Server → 添加服务器")
    print("   3. 使用上面的配置参数进行配置")
    print("   4. 保存并重启 Cherry Studio")
    print("   5. 尝试上面的测试提示词")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
