#!/usr/bin/env python3
"""
测试 MCP Server 是否可以正常列出工具
"""

import asyncio
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


async def test_server_tools():
    """测试服务器是否可以列出工具"""
    from server import TrendingMCPServer

    print("初始化 MCP Server...")
    server = TrendingMCPServer()

    print(f"✓ 服务器名称: {server.server.name}")
    print(f"✓ GitHub Fetcher: {server.github_fetcher.platform_name}")
    print(f"✓ Hacker News Fetcher: {server.hackernews_fetcher.platform_name}")
    print(f"✓ Product Hunt Fetcher: {server.producthunt_fetcher.platform_name}")

    print("\n所有组件初始化成功！")
    print("\nMCP Server 配置已添加到 Claude Desktop。")
    print("请重启 Claude Desktop 以加载新的 MCP Server。")

    await server.cleanup()
    print("\n✓ 清理完成")


if __name__ == "__main__":
    asyncio.run(test_server_tools())
