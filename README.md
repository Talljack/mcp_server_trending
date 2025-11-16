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
- 💰 **Indie Hackers** - 收入报告和社区讨论
- 🌐 **Reddit** - 热门帖子和社区
- 🤖 **OpenRouter** - LLM 模型排行榜
- 💵 **TrustMRR** - MRR/收入排行榜
- 🔧 **AI Tools Directory** - 热门 AI 工具
- 🤗 **HuggingFace** - ML 模型和数据集

> 专为独立开发者、Indie Hackers 和技术创业者设计
> **✅ 所有平台无需配置 API Token！**

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
      "command": "mcp-server-trending",
      "env": {
        "OPENROUTER_API_KEY": "your_openrouter_api_key_here",
        "HUGGINGFACE_TOKEN": "your_huggingface_token_here"
      }
    }
  }
}
```

**如果不需要 OpenRouter/HuggingFace 功能**，可以省略 `env` 配置：

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
  "command": "mcp-server-trending",
  "env": {
    "OPENROUTER_API_KEY": "your_openrouter_api_key_here"
  }
}
```

**如果不需要 OpenRouter 功能**，可以省略 `env` 字段。

**注意**：如果是从源码安装，command 需要使用完整路径：
```json
{
  "command": "/path/to/mcp_server_trending/.venv/bin/mcp-server-trending",
  "env": {
    "OPENROUTER_API_KEY": "your_openrouter_api_key_here"
  }
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
        "OPENROUTER_API_KEY": "your_openrouter_api_key_here"
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
        "OPENROUTER_API_KEY": "your_openrouter_api_key_here"
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
        "OPENROUTER_API_KEY": "your_openrouter_api_key_here"
      }
    }
  ]
}
```

**所有客户端都支持 `env` 配置！** ✅

---

## 🔧 配置说明

### OpenRouter API Key (可选)

如果你想使用 OpenRouter 相关功能（LLM 模型排行榜），需要配置 API Key：

1. **获取 API Key**
   - 访问 https://openrouter.ai/keys
   - 注册并获取 API Key（有免费额度）

2. **配置方法**

**方式一：在 MCP 配置中添加（推荐）**

直接在 Claude Desktop 或 Cherry Studio 的配置文件中添加 `env` 字段：

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "env": {
        "OPENROUTER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**方式二：使用 .env 文件**
```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件，添加你的 API key
echo "OPENROUTER_API_KEY=your_api_key_here" >> .env
```

**方式三：环境变量**
```bash
export OPENROUTER_API_KEY=your_api_key_here
mcp-server-trending
```

**注意**:
- ✅ 如果不配置 API Key，其他平台（GitHub、Hacker News 等）仍然正常工作
- ⚠️ 调用 OpenRouter tools 时会返回明确的配置提示
- 🆓 OpenRouter 提供免费额度，足够个人使用

### HuggingFace Token (可选)

如果你想提高 HuggingFace API 的请求限制，可以配置 Token：

1. **获取 Token**
   - 访问 https://huggingface.co/settings/tokens
   - 创建一个 Read Token

2. **配置方法**

**方式一：在 MCP 配置中添加（推荐）**

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "env": {
        "HUGGINGFACE_TOKEN": "your_token_here"
      }
    }
  }
}
```

**方式二：使用 .env 文件**
```bash
echo "HUGGINGFACE_TOKEN=your_token_here" >> .env
```

**注意**:
- ✅ HuggingFace Token 完全可选，不配置也能正常使用
- ⚠️ 公开 API 有请求频率限制，Token 可提高限制
- 🆓 HuggingFace Token 免费，无需付费

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

```
帮我对比一下最流行的 LLM 模型（需要配置 OpenRouter API Key）
```

---

## 🎯 功能特性

### 已支持平台

| 平台 | 功能 | 需要 Token? |
|------|------|-------------|
| **GitHub Trending** | 热门仓库/开发者 | ❌ 可选 |
| **Hacker News** | 各类热门故事 | ❌ 不需要 |
| **Product Hunt** | 产品发布 | ❌ 不需要 |
| **Indie Hackers** | 收入报告/热门讨论 | ❌ 不需要 |
| **Reddit** | 热门帖子/社区 | ❌ 不需要 |
| **OpenRouter** | LLM 模型排行榜 | ⚠️ **需要 API Key** |
| **TrustMRR** | MRR/收入排行榜 | ❌ 不需要 |
| **AI Tools Directory** | 热门 AI 工具 | ❌ 不需要 |
| **HuggingFace** | ML 模型/数据集 | ❌ 可选 |

### 可用工具 (15个)

**GitHub**
- `get_github_trending_repos` - 获取 GitHub trending 仓库
- `get_github_trending_developers` - 获取 GitHub trending 开发者

**Hacker News**
- `get_hackernews_stories` - 获取 Hacker News 故事

**Product Hunt**
- `get_producthunt_products` - 获取 Product Hunt 产品

**Indie Hackers**
- `get_indiehackers_popular` - 获取热门讨论
- `get_indiehackers_income_reports` - 获取收入报告 💰

**Reddit**
- `get_reddit_trending` - 获取热门帖子
- `get_reddit_search` - 搜索帖子

**OpenRouter** ⚠️ **需要 API Key**
- `get_openrouter_models` - 获取 LLM 模型列表
- `get_openrouter_rankings` - 获取模型排行榜
- `get_openrouter_compare` - 比较模型

**TrustMRR**
- `get_trustmrr_rankings` - 获取 MRR/收入排行榜 💵

**AI Tools Directory**
- `get_ai_tools` - 获取热门 AI 工具 🔧

**HuggingFace** (可选 Token)
- `get_huggingface_models` - 获取热门 ML 模型 🤗
- `get_huggingface_datasets` - 获取热门数据集 📊

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
