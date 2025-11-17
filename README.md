# MCP Server Trending

<div align="center">

**🎯 一站式独立开发者热门榜单聚合服务**

[![CI](https://github.com/Talljack/mcp_server_trending/workflows/CI/badge.svg)](https://github.com/Talljack/mcp_server_trending/actions)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

*让 AI 助手帮你追踪全球热门技术内容*

[快速开始](#-快速开始) • [功能特性](#-功能特性) • [文档](#-文档)

</div>

---

## 🌟 项目简介

MCP Server Trending 是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的热门榜单聚合服务，让你的 AI 助手能够实时查询：

- 📊 **GitHub Trending** - 热门仓库和开发者
- 💬 **Hacker News** - 技术社区热门讨论
- 🚀 **Product Hunt** - 最新产品发布
- 💰 **Indie Hackers** - 收入报告和社区讨论
- 🤖 **OpenRouter** - LLM 模型排行榜
- 💵 **TrustMRR** - MRR/收入排行榜
- 🔧 **AI Tools Directory** - 热门 AI 工具
- 🤗 **HuggingFace** - ML 模型和数据集
- 🇨🇳 **V2EX** - 中文创意工作者社区
- 📝 **掘金 (Juejin)** - 中文技术社区
- 🌍 **dev.to** - 国际开发者社区
- 🔮 **ModelScope** - 魔塔社区 AI 模型与数据集
- 📈 **Stack Overflow Trends** - 技术标签趋势
- ⭐ **Awesome Lists** - GitHub 精选资源列表

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

**最小配置（大部分平台可用）**：
```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending"
    }
  }
}
```

**完整配置（启用所有平台）**：
```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "env": {
        "PRODUCTHUNT_CLIENT_ID": "your_producthunt_client_id",
        "PRODUCTHUNT_CLIENT_SECRET": "your_producthunt_client_secret",
        "HUGGINGFACE_TOKEN": "your_huggingface_token"
      }
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
  "command": "mcp-server-trending",
  "env": {
    "PRODUCTHUNT_CLIENT_ID": "your_producthunt_client_id",
    "PRODUCTHUNT_CLIENT_SECRET": "your_producthunt_client_secret"
  }
}
```

**注意**：如果是从源码安装，command 需要使用完整路径：
```json
{
  "command": "/path/to/mcp_server_trending/.venv/bin/mcp-server-trending"
}
```

#### Cursor

在项目根目录创建 `.cursor/mcp.json`（项目级）或 `~/.cursor/mcp.json`（全局）:

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "args": [],
      "env": {
        "PRODUCTHUNT_CLIENT_ID": "your_producthunt_client_id",
        "PRODUCTHUNT_CLIENT_SECRET": "your_producthunt_client_secret"
      }
    }
  }
}
```

#### Cline (VSCode)

打开 Cline 扩展 → MCP Servers → Configure MCP Servers:

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "args": [],
      "env": {
        "PRODUCTHUNT_CLIENT_ID": "your_producthunt_client_id",
        "PRODUCTHUNT_CLIENT_SECRET": "your_producthunt_client_secret"
      },
      "alwaysAllow": [],
      "disabled": false
    }
  }
}
```

#### Continue (VSCode/JetBrains)

在 Continue 配置中添加:

```json
{
  "mcpServers": [
    {
      "name": "trending",
      "command": "mcp-server-trending",
      "env": {
        "PRODUCTHUNT_CLIENT_ID": "your_producthunt_client_id",
        "PRODUCTHUNT_CLIENT_SECRET": "your_producthunt_client_secret"
      }
    }
  ]
}
```

**所有客户端都支持 `env` 配置！** ✅

---

## 🔧 环境变量配置

### 可选配置（按需添加）

#### 1. Product Hunt API Credentials（可选，获取真实产品数据）

**获取方式**：
1. 访问 https://www.producthunt.com/v2/oauth/applications
2. 创建一个新应用 (Create a new application)
3. 复制 **Client ID** 和 **Client Secret**

**配置方法**：

**方式一：在 MCP 配置中添加（推荐）**
```json
{
  "env": {
    "PRODUCTHUNT_CLIENT_ID": "your_client_id_here",
    "PRODUCTHUNT_CLIENT_SECRET": "your_client_secret_here"
  }
}
```

**方式二：使用 .env 文件**
```bash
cp .env.example .env
# 编辑 .env 文件
PRODUCTHUNT_CLIENT_ID=your_client_id_here
PRODUCTHUNT_CLIENT_SECRET=your_client_secret_here
```

**注意**：
- ✅ 不配置会返回友好的占位数据和设置说明
- ✅ 配置后可获取真实的产品数据、投票数、评论数等
- 🆓 Product Hunt API 免费使用

---

#### 2. HuggingFace Token（可选，提高请求限制）

**获取方式**：
1. 访问 https://huggingface.co/settings/tokens
2. 创建一个 Read Token

**配置方法**：

**方式一：在 MCP 配置中添加（推荐）**
```json
{
  "env": {
    "HUGGINGFACE_TOKEN": "your_token_here"
  }
}
```

**方式二：使用 .env 文件**
```bash
echo "HUGGINGFACE_TOKEN=your_token_here" >> .env
```

**注意**：
- ✅ 完全可选，不配置也能正常使用
- ⚠️ 公开 API 有请求频率限制，Token 可提高限制
- 🆓 HuggingFace Token 免费

---

#### 3. GitHub Token（可选，提高请求限制）

**获取方式**：
1. 访问 https://github.com/settings/tokens
2. 创建一个 Personal Access Token

**配置方法**：
```json
{
  "env": {
    "GITHUB_TOKEN": "your_token_here"
  }
}
```

**注意**：
- ✅ 完全可选，不配置也能正常使用
- ⚠️ Token 可提高 GitHub API 请求限制
- 🆓 GitHub Token 免费

---

### 完整环境变量示例

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "env": {
        "PRODUCTHUNT_CLIENT_ID": "your_producthunt_client_id",
        "PRODUCTHUNT_CLIENT_SECRET": "your_producthunt_client_secret",
        "HUGGINGFACE_TOKEN": "your_huggingface_token",
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  }
}
```

**提示**：只需要配置你需要的平台，其他可以省略！

---

## 💬 使用示例

```
请帮我查询 GitHub 上今天最热门的 Python 项目
```

```
Hacker News 上现在有什么热门的技术讨论？
```

```
帮我看看 Product Hunt 今天有哪些有趣的产品（需要配置 Product Hunt API）
```

```
对比一下掘金和 dev.to 上的热门技术文章
```

```
查询 Stack Overflow 上最热门的技术标签
```

```
帮我找一些 Python 相关的 Awesome 列表
```

---

## 🎯 功能特性

### 已支持平台

| 平台 | 功能 | 状态 | 需要配置? |
|------|------|------|----------|
| **GitHub Trending** | 热门仓库/开发者 | ✅ 完全可用 | ❌ 可选 Token |
| **Hacker News** | 各类热门故事 | ✅ 完全可用 | ❌ 不需要 |
| **Product Hunt** | 产品发布 | ⚠️ 需配置 API* | ⚠️ 需要 Client ID/Secret |
| **Indie Hackers** | 收入报告 | ✅ 真实数据 (Firebase) | ❌ 不需要 |
| **Indie Hackers** | 热门讨论 | ✅ 真实数据 (Firebase) | ❌ 不需要 |
| **OpenRouter** | LLM 模型排行榜 | ⚠️ 需配置 API Key* | ⚠️ 需要 API Key |
| **TrustMRR** | MRR/收入排行榜 | ✅ 完全可用 | ❌ 不需要 |
| **AI Tools Directory** | 热门 AI 工具 | ✅ 完全可用 | ❌ 不需要 |
| **HuggingFace** | ML 模型/数据集 | ✅ 完全可用 | ❌ 可选 Token |
| **V2EX** | 中文社区热门话题 | ✅ 完全可用 | ❌ 不需要 |
| **掘金 (Juejin)** | 中文技术文章 | ✅ 完全可用 | ❌ 不需要 |
| **dev.to** | 国际开发者文章 | ✅ 完全可用 | ❌ 不需要 |
| **ModelScope** | 魔塔 AI 模型/数据集 | ✅ 完全可用 | ❌ 不需要 |
| **Stack Overflow Trends** | 技术标签趋势 | ✅ 完全可用 | ❌ 不需要 |
| **Awesome Lists** | GitHub 精选列表 | ✅ 完全可用 | ❌ 可选 Token |

> \* **说明**：
> - Product Hunt 需要配置 API credentials 才能获取真实数据，否则返回占位数据和配置指引
> - OpenRouter 需要配置 API Key 才能使用，未配置时返回错误提示和配置说明

### 可用工具 (22个)

**GitHub** (2个)
- `get_github_trending_repos` - 获取 GitHub trending 仓库
- `get_github_trending_developers` - 获取 GitHub trending 开发者

**Hacker News** (1个)
- `get_hackernews_stories` - 获取 Hacker News 故事

**Product Hunt** (1个)
- `get_producthunt_products` - 获取 Product Hunt 产品（需配置 API）

**Indie Hackers** (2个)
- `get_indiehackers_popular` - 获取热门讨论（真实数据）
- `get_indiehackers_income_reports` - 获取收入报告 💰（真实数据）

**OpenRouter** (3个) 🤖
- `get_openrouter_models` - 获取所有 LLM 模型列表（需配置 API Key）
- `get_openrouter_popular` - 获取最受欢迎模型
- `get_openrouter_best_value` - 获取最佳性价比模型

**TrustMRR** (1个)
- `get_trustmrr_rankings` - 获取 MRR/收入排行榜 💵

**AI Tools Directory** (1个)
- `get_ai_tools` - 获取热门 AI 工具 🔧

**HuggingFace** (2个)
- `get_huggingface_models` - 获取热门 ML 模型 🤗
- `get_huggingface_datasets` - 获取热门数据集 📊

**V2EX** (1个) 🇨🇳
- `get_v2ex_hot_topics` - 获取热门话题

**掘金 (Juejin)** (1个) 📝
- `get_juejin_articles` - 获取推荐技术文章

**dev.to** (1个) 🌍
- `get_devto_articles` - 获取开发者文章

**ModelScope** (2个) 🔮
- `get_modelscope_models` - 获取魔塔社区热门模型
- `get_modelscope_datasets` - 获取魔塔社区热门数据集

**Stack Overflow** (1个) 📈
- `get_stackoverflow_trends` - 获取 Stack Overflow 热门技术标签

**Awesome Lists** (1个) ⭐
- `get_awesome_lists` - 获取 GitHub Awesome 精选列表

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

## 数据来源声明

本项目从以下平台聚合公开数据：
- 仅获取公开展示的信息（标题、摘要、链接）
- 提供原文链接，引导用户访问原网站
- 实现了缓存机制，避免频繁请求
- 不存储完整内容，不用于商业目的

如有任何问题，请联系我们。
