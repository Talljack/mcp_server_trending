# 📍 MCP Server Trending - Smithery Information

> **Welcome from Smithery!** 👋

## 🎯 What is this?

**MCP Server Trending** is a comprehensive trending data aggregation service for indie developers, built on the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/).

It provides **45+ tools** across **25+ platforms** including:
- 📊 GitHub Trending
- 💬 Hacker News
- 🚀 Product Hunt
- 📚 Papers with Code
- 🤖 Replicate AI Models
- 💼 Remote Jobs
- 🔬 Research Papers (arXiv, Semantic Scholar, OpenReview)
- And many more!

## ⚠️ Important: Local Installation Required

This is a **stdio-mode MCP server**, which means:
- ✅ **Designed for local installation** (not cloud-hosted)
- ✅ **Zero cost** - no server fees
- ✅ **Zero maintenance** - no uptime to worry about
- ✅ **Better security** - runs on your machine
- ✅ **Faster response** - no network latency

**Why no Smithery deployment?**
- Smithery's hosted deployment expects HTTP/SSE mode servers
- Our stdio mode is optimized for desktop AI clients (Claude Desktop, Cursor, etc.)

## 🚀 Quick Installation

### Option 1: PyPI (Recommended)

```bash
# Install with pipx
pipx install mcp-server-trending

# macOS/Linux: Create system symlink
sudo ln -sf ~/.local/pipx/venvs/mcp-server-trending/bin/mcp-server-trending /usr/local/bin/mcp-server-trending
```

### Option 2: From Source

```bash
git clone https://github.com/Talljack/mcp_server_trending.git
cd mcp_server_trending
bash install.sh
```

## 📖 Configuration

Add to your AI client config (e.g., Claude Desktop, Cursor):

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "env": {
        "HUGGINGFACE_TOKEN": "optional_token",
        "GITHUB_TOKEN": "optional_token"
      }
    }
  }
}
```

## 🎯 What You Get

### 45+ MCP Tools Including:

**Developer Platforms:**
- GitHub Trending (repos & developers)
- Stack Overflow Trends
- npm & PyPI Packages
- VS Code & Chrome Extensions

**Tech Communities:**
- Hacker News
- Lobsters
- Echo JS (JavaScript news)
- dev.to & 掘金 (Juejin)

**AI & Research:**
- Papers with Code (via HuggingFace)
- arXiv Papers
- Semantic Scholar
- OpenReview (ML conferences)
- HuggingFace Models & Datasets
- Replicate AI Models

**Indie Hacker Resources:**
- Indie Hackers (income reports & discussions)
- Product Hunt
- Betalist (early startups)
- TrustMRR (revenue rankings)
- Remote Jobs (RemoteOK, We Work Remotely)

**Aggregation Tools:**
- Tech Stack Analysis (cross-platform)
- Indie Revenue Dashboard
- Topic Trend Tracking

## 📚 Full Documentation

- **GitHub**: https://github.com/Talljack/mcp_server_trending
- **README**: https://github.com/Talljack/mcp_server_trending#readme
- **Installation Guide**: Detailed steps for all platforms
- **API Reference**: All 45+ tools documented

## 🤝 Support & Contributing

- **Issues**: https://github.com/Talljack/mcp_server_trending/issues
- **Contributing**: https://github.com/Talljack/mcp_server_trending/blob/main/CONTRIBUTING.md
- **License**: MIT

## ⭐ Why Choose This?

- ✅ **Comprehensive** - 25+ platforms in one service
- ✅ **Fast** - Smart caching reduces API calls
- ✅ **Free** - No API keys required for most platforms
- ✅ **Open Source** - MIT licensed
- ✅ **Well Maintained** - Active development
- ✅ **Type Safe** - Full Python type hints

---

**Made with ❤️ for Indie Hackers**

If you find this useful, please give us a ⭐ on GitHub!

