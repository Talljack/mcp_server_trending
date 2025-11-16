"""MCP Server Trending - 独立开发者热门榜单服务"""

try:
    from importlib.metadata import version

    __version__ = version("mcp-server-trending")
except Exception:
    __version__ = "0.1.0"  # fallback

__author__ = "MCP Server Trending Team"
