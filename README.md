# MCP Server Trending

<div align="center">

**🎯 一站式独立开发者热门榜单聚合服务**

[![CI](https://github.com/Talljack/mcp_server_trending/workflows/CI/badge.svg)](https://github.com/Talljack/mcp_server_trending/actions)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

*让 AI 助手帮你追踪 GitHub、Hacker News、Product Hunt 的热门内容*

[快速开始](#-快速开始) • [功能特性](#-功能特性) • [文档](#-文档)

</div>

---

## 🌟 项目简介

MCP Server Trending 是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的热门榜单聚合服务，让你的 AI 助手能够实时查询：

- 📊 **GitHub Trending** - 热门仓库和开发者
- 💬 **Hacker News** - 技术社区热门讨论
- 🚀 **Product Hunt** - 最新产品发布

> 专为独立开发者、Indie Hackers 和技术创业者设计

---

## ⚡ 快速开始

### 方式一：从 PyPI 安装（推荐）

```bash
pip install mcp-server-trending
```

> **注意**：首次发布前，请使用方式二从源码安装

### 方式二：从源码安装

```bash
git clone https://github.com/Talljack/mcp_server_trending.git
cd mcp_server_trending
bash install.sh
```

**就这么简单！** 🎉 脚本会自动完成所有配置。

### 配置 AI 客户端

#### Claude Desktop (MacOS)

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending"
    }
  }
}
```

**重启 Claude Desktop 即可使用！**

#### Cherry Studio

在 Cherry Studio → 设置 → MCP Server 中添加:

```json
{
  "name": "Trending",
  "description": "独立开发者热门榜单聚合服务",
  "type": "stdio",
  "command": "mcp-server-trending"
}
```

**注意**：如果是从源码安装，command 需要使用完整路径：
```json
{
  "command": "/path/to/mcp_server_trending/.venv/bin/mcp-server-trending"
}
```

---

## 💬 使用示例

```
请帮我查询 GitHub 上今天最热门的 Python 项目
```

```
Hacker News 上现在有什么热门的技术讨论？
```

```
同时告诉我 GitHub 上的 Rust 项目和 Hacker News 的技术热点
```

---

## 🎯 功能特性

### 已支持平台

| 平台 | 功能 | 可调参数 |
|------|------|---------|
| **GitHub Trending** | 热门仓库/开发者 | 语言、时间范围 |
| **Hacker News** | 各类热门故事 | 类型、数量(1-500) |
| **Product Hunt** | 产品发布 | 时间范围、主题 |

### 可用工具

- `get_github_trending_repos` - 获取 GitHub trending 仓库
- `get_github_trending_developers` - 获取 GitHub trending 开发者
- `get_hackernews_stories` - 获取 Hacker News 故事
- `get_producthunt_products` - 获取 Product Hunt 产品

---

## 🏗️ 技术架构

- **语言**: Python 3.10+
- **协议**: Model Context Protocol (MCP)
- **设计**: 高复用性 + 模块化 + 类型安全
- **部署**: 一键安装脚本 + GitHub Actions CI

---

## 📚 文档

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - 贡献指南
- **[CHERRY_STUDIO_QUICKSTART.md](CHERRY_STUDIO_QUICKSTART.md)** - Cherry Studio 配置
- **[PRD.md](PRD.md)** - 产品需求文档

---

## 🛠️ 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 代码格式化
black src/ tests/
ruff check src/ tests/
```

---

## 🤝 贡献

欢迎贡献！查看 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

MIT License - 查看 [LICENSE](LICENSE)

---

<div align="center">

**如果觉得有用，请给个 ⭐️！**

Made with ❤️ for Indie Hackers

</div>
