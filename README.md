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

MCP Server Trending 是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的热门榜单聚合服务,让你的 AI 助手能够实时查询：

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
- 🧩 **VS Code Extensions** - Visual Studio Marketplace 热门扩展
- 📦 **npm Packages** - npm 热门 JavaScript/Node.js 包
- 🔌 **Chrome Extensions** - Chrome Web Store 热门扩展
- 🐍 **PyPI Packages** - Python 包热门排行
- 💼 **RemoteOK Jobs** - 远程工作机会
- 🔌 **WordPress Plugins** - WordPress 插件目录
- 📄 **arXiv Papers** - 科研论文预印本平台
- 🎓 **Semantic Scholar** - AI 驱动的学术搜索引擎
- 🏆 **OpenReview** - ML 会议论文评审平台
- 🔬 **Aggregation Analysis** - 跨平台聚合分析工具

> 专为独立开发者、Indie Hackers 和技术创业者设计

---

## ⚡ 快速开始

### 方式一：使用 Smithery 安装（推荐）

[Smithery](https://smithery.ai/) 是一个 MCP 服务器管理平台，可以一键安装到任何支持的客户端。

```bash
npx -y @smithery/cli install mcp-server-trending --client <CLIENT_NAME>
```

支持的客户端：`claude-desktop`、`cursor`、`cline`、`windsurf`、`zed` 等

### 方式二：从 PyPI 安装

```bash
pip install mcp-server-trending
```

> **注意**：首次发布前，请使用方式三从源码安装

### 方式三：从源码安装

```bash
git clone https://github.com/Talljack/mcp_server_trending.git
cd mcp_server_trending
bash install.sh
```

**就这么简单！** 🎉 脚本会自动完成所有配置。

---

## 🖥️ 支持的客户端

我们支持所有主流的 AI 编辑器和工具：

| 类别 | 客户端 | 配置方式 | 官方文档 |
|------|--------|---------|---------|
| **AI 桌面应用** | Claude Desktop | JSON 配置 | [文档](https://modelcontextprotocol.io/quickstart/user) |
| | Cherry Studio | JSON 配置 | - |
| **代码编辑器** | Cursor | `.cursor/mcp.json` | [文档](https://docs.cursor.com/context/model-context-protocol) |
| | Windsurf | JSON 配置 | [文档](https://docs.windsurf.com/windsurf/cascade/mcp) |
| | Zed | `settings.json` | [文档](https://zed.dev/docs/assistant/context-servers) |
| **VS Code 扩展** | Cline | MCP 配置 | - |
| | Continue | JSON 配置 | [文档](https://docs.continue.dev/features/model-context-protocol) |
| | Roo Code | JSON 配置 | [文档](https://docs.roocode.com/features/mcp/using-mcp-in-roo) |
| **JetBrains** | AI Assistant | MCP 设置 | [文档](https://www.jetbrains.com/help/ai-assistant/configure-an-mcp-server.html) |
| **AI 工具** | Claude Code | CLI 命令 | [文档](https://docs.anthropic.com/en/docs/claude-code/mcp) |
| | Amazon Q Developer | JSON 配置 | [文档](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-mcp-configuration.html) |
| | Augment Code | UI 或 JSON | - |
| | Kiro | MCP 设置 | [文档](https://kiro.dev/docs/mcp/configuration/) |
| **终端工具** | Warp | MCP 设置 | [文档](https://docs.warp.dev/knowledge-and-collaboration/mcp) |

> 💡 **提示**：点击下方的配置说明查看详细的安装步骤

---

### 配置 AI 客户端

> **提示**：所有客户端都支持 `env` 配置！✅

<details>
<summary><b>Claude Desktop</b></summary>

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
        "HUGGINGFACE_TOKEN": "your_huggingface_token",
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  }
}
```

**重启 Claude Desktop 即可使用！**

</details>

<details>
<summary><b>Claude Code</b></summary>

运行以下命令添加 MCP 服务器。查看 [Claude Code MCP 文档](https://docs.anthropic.com/en/docs/claude-code/mcp) 了解更多。

```sh
claude mcp add trending -- mcp-server-trending
```

**带环境变量的配置**：
```sh
```

</details>

<details>
<summary><b>Cursor</b></summary>

在项目根目录创建 `.cursor/mcp.json`（项目级）或 `~/.cursor/mcp.json`（全局）。查看 [Cursor MCP 文档](https://docs.cursor.com/context/model-context-protocol) 了解更多。

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "args": [],
      "env": {
        
        "HUGGINGFACE_TOKEN": "your_huggingface_token",
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  }
}
```

**注意**：如果是从源码安装，command 需要使用完整路径：
```json
{
  "mcpServers": {
    "trending": {
      "command": "/path/to/mcp_server_trending/.venv/bin/mcp-server-trending",
      "args": []
    }
  }
}
```

</details>

<details>
<summary><b>Windsurf</b></summary>

添加到 Windsurf MCP 配置文件。查看 [Windsurf MCP 文档](https://docs.windsurf.com/windsurf/cascade/mcp) 了解更多。

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "args": [],
      "env": {
        
        "HUGGINGFACE_TOKEN": "your_huggingface_token",
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  }
}
```

</details>

<details>
<summary><b>VS Code (Cline)</b></summary>

打开 Cline 扩展 → MCP Servers → Configure MCP Servers:

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "args": [],
      "env": {
        
        "HUGGINGFACE_TOKEN": "your_huggingface_token",
        "GITHUB_TOKEN": "your_github_token"
      },
      "alwaysAllow": [],
      "disabled": false
    }
  }
}
```

</details>

<details>
<summary><b>VS Code (Continue)</b></summary>

在 Continue 配置中添加。查看 [Continue 文档](https://docs.continue.dev/features/model-context-protocol) 了解更多。

```json
{
  "mcpServers": [
    {
      "name": "trending",
      "command": "mcp-server-trending",
      "env": {
        
        "HUGGINGFACE_TOKEN": "your_huggingface_token",
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  ]
}
```

</details>

<details>
<summary><b>Zed</b></summary>

添加到 Zed `settings.json`。查看 [Zed Context Server 文档](https://zed.dev/docs/assistant/context-servers) 了解更多。

```json
{
  "context_servers": {
    "mcp-server-trending": {
      "source": "custom",
      "command": "mcp-server-trending",
      "args": [],
      "env": {
        
        "HUGGINGFACE_TOKEN": "your_token",
        "GITHUB_TOKEN": "your_token"
      }
    }
  }
}
```

</details>

<details>
<summary><b>JetBrains AI Assistant</b></summary>

查看 [JetBrains AI Assistant 文档](https://www.jetbrains.com/help/ai-assistant/configure-an-mcp-server.html) 了解更多。

1. 在 JetBrains IDE 中，进入 `Settings` → `Tools` → `AI Assistant` → `Model Context Protocol (MCP)`
2. 点击 `+ Add`
3. 在对话框左上角点击 `Command`，从列表中选择 `As JSON` 选项
4. 添加以下配置并点击 `OK`：

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "args": [],
      "env": {
        
        "HUGGINGFACE_TOKEN": "your_huggingface_token",
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  }
}
```

5. 点击 `Apply` 保存更改

</details>

<details>
<summary><b>Cherry Studio</b></summary>

在 Cherry Studio → 设置 → MCP Server 中添加:

```json
{
  "name": "Trending",
  "description": "独立开发者热门榜单聚合服务",
  "type": "stdio",
  "command": "mcp-server-trending",
  "env": {
    
    "HUGGINGFACE_TOKEN": "your_huggingface_token",
    "GITHUB_TOKEN": "your_github_token"
  }
}
```

**注意**：如果是从源码安装，command 需要使用完整路径：
```json
{
  "command": "/path/to/mcp_server_trending/.venv/bin/mcp-server-trending"
}
```

</details>

<details>
<summary><b>Roo Code</b></summary>

添加到 Roo Code MCP 配置文件。查看 [Roo Code MCP 文档](https://docs.roocode.com/features/mcp/using-mcp-in-roo) 了解更多。

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "args": [],
      "env": {
        
        "HUGGINGFACE_TOKEN": "your_huggingface_token",
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Amazon Q Developer CLI</b></summary>

添加到 Amazon Q Developer CLI 配置文件。查看 [Amazon Q Developer CLI 文档](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-mcp-configuration.html) 了解更多。

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "args": [],
      "env": {
        
        "HUGGINGFACE_TOKEN": "your_huggingface_token",
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Warp</b></summary>

查看 [Warp Model Context Protocol 文档](https://docs.warp.dev/knowledge-and-collaboration/mcp#adding-an-mcp-server) 了解更多。

1. 进入 `Settings` → `AI` → `Manage MCP servers`
2. 点击 `+ Add` 按钮添加新的 MCP 服务器
3. 粘贴以下配置：

```json
{
  "trending": {
    "command": "mcp-server-trending",
    "args": [],
    "env": {
      
      "HUGGINGFACE_TOKEN": "your_huggingface_token",
      "GITHUB_TOKEN": "your_github_token"
    },
    "working_directory": null,
    "start_on_launch": true
  }
}
```

4. 点击 `Save` 保存更改

</details>

<details>
<summary><b>Augment Code</b></summary>

**使用界面配置**：

1. 点击汉堡菜单
2. 选择 **Settings**
3. 进入 **Tools** 部分
4. 点击 **+ Add MCP** 按钮
5. 输入命令：`mcp-server-trending`
6. 命名为 **Trending**
7. 点击 **Add** 按钮

**手动配置**：

1. 按 Cmd/Ctrl + Shift + P 或进入 Augment 面板的汉堡菜单
2. 选择 Edit Settings
3. 在 Advanced 下，点击 Edit in settings.json
4. 在 `augment.advanced` 对象的 `mcpServers` 数组中添加服务器配置：

```json
"augment.advanced": {
  "mcpServers": [
    {
      "name": "trending",
      "command": "mcp-server-trending",
      "args": [],
      "env": {
        
        "HUGGINGFACE_TOKEN": "your_huggingface_token",
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  ]
}
```

</details>

<details>
<summary><b>Kiro</b></summary>

查看 [Kiro Model Context Protocol 文档](https://kiro.dev/docs/mcp/configuration/) 了解更多。

1. 进入 `Kiro` → `MCP Servers`
2. 点击 `+ Add` 按钮添加新的 MCP 服务器
3. 粘贴以下配置：

```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending",
      "args": [],
      "env": {
        
        "HUGGINGFACE_TOKEN": "your_huggingface_token",
        "GITHUB_TOKEN": "your_github_token"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

4. 点击 `Save` 保存更改

</details>

<details>
<summary><b>从源码安装时的配置</b></summary>

如果你是从源码安装的，需要在 `command` 中使用完整路径指向虚拟环境中的可执行文件：

**找到可执行文件路径**：
```bash
which mcp-server-trending
# 或者
cd mcp_server_trending && echo "$(pwd)/.venv/bin/mcp-server-trending"
```

**配置示例**：
```json
{
  "mcpServers": {
    "trending": {
      "command": "/path/to/mcp_server_trending/.venv/bin/mcp-server-trending",
      "args": [],
      "env": {
      }
    }
  }
}
```

</details>

---

## 🔧 环境变量配置

### 可选配置（按需添加）

#### 1. HuggingFace Token（可选，提高请求限制）

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

#### 2. GitHub Token（可选，提高请求限制）

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

**基础查询示例：**

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

```
查看 VS Code 最热门的扩展有哪些
```

```
帮我找最受欢迎的 React 相关 npm 包
```

```
Chrome 浏览器有什么好用的生产力扩展？
```

**新增功能示例：**

```
查看 PyPI 上最热门的 Python 包
```

```
帮我找一些远程工作机会，要求是 Python 开发
```

```
WordPress 有哪些热门的 SEO 插件？
```

**聚合分析示例：**

```
分析一下 Next.js 在各个平台的流行度
```

```
给我看看独立开发者的收入仪表板
```

```
追踪一下 AI Agents 这个话题在各个平台的热度
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
| **VS Code Extensions** | 热门扩展 | ✅ 完全可用 | ❌ 不需要 |
| **npm Packages** | JavaScript/Node.js 包 | ✅ 完全可用 | ❌ 不需要 |
| **Chrome Extensions** | 浏览器扩展（精选数据）| ✅ 完全可用 | ❌ 不需要 |
| **PyPI Packages** | Python 包下载排行 | ✅ 完全可用 | ❌ 不需要 |
| **RemoteOK Jobs** | 远程工作职位 | ✅ 完全可用* | ❌ 不需要 |
| **WordPress Plugins** | WordPress 插件 | ✅ 完全可用 | ❌ 不需要 |
| **arXiv Papers** | 科研论文预印本 | ✅ 完全可用 | ❌ 不需要 |
| **Semantic Scholar** | 学术搜索引擎 | ✅ 完全可用 | ❌ 不需要 |
| **OpenReview** | ML 会议论文评审 | ✅ 完全可用 | ❌ 不需要 |

> \* **说明**：
> - Product Hunt 需要配置 API credentials 才能获取真实数据，否则返回占位数据和配置指引
> - OpenRouter 需要配置 API Key 才能使用，未配置时返回错误提示和配置说明
> - **RemoteOK** 使用官方公开 JSON API (`https://remoteok.com/api`)，完全免费无需认证
>   - ✅ API 格式：第一条是表头，职位数据从第二条开始
>   - ⚠️ 网络要求：RemoteOK 会阻止 VPN/代理访问，如遇到 "Disable your VPN" 错误：
>     - 关闭 VPN 或代理软件
>     - 使用非数据中心 IP（家庭网络、手机热点等）
>     - 代码已实现智能降级：API 失败时自动尝试网页抓取

### 可用工具 (34个)

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

**VS Code Extensions** (1个) 🧩
- `get_vscode_extensions` - 获取 Visual Studio Marketplace 热门扩展

**npm Packages** (1个) 📦
- `get_npm_packages` - 获取 npm 热门 JavaScript/Node.js 包

**Chrome Extensions** (1个) 🔌
- `get_chrome_extensions` - 获取 Chrome Web Store 热门扩展（精选数据）

**PyPI Packages** (1个) 🐍
- `get_pypi_packages` - 获取 Python 包下载排行

**RemoteOK Jobs** (1个) 💼
- `get_remote_jobs` - 获取远程工作职位

**WordPress Plugins** (1个) 🔌
- `get_wordpress_plugins` - 获取 WordPress 插件目录热门插件

**Research Papers** (3个) 📄
- `get_arxiv_papers` - 获取 arXiv 科研论文（支持分类、关键词搜索）
- `search_semantic_scholar` - 搜索 Semantic Scholar 学术论文（AI 驱动、引用指标）
- `get_openreview_papers` - 获取 OpenReview ML 会议论文（ICLR、NeurIPS、ICML 等）

**Aggregation Analysis** (3个) 🔬
- `analyze_tech_stack` - 跨平台技术栈分析（GitHub + npm + PyPI + Stack Overflow + VS Code + Jobs）
- `get_indie_revenue_dashboard` - 独立开发者收入仪表板（Indie Hackers + TrustMRR）
- `track_topic_trends` - 话题趋势追踪（Hacker News + GitHub + Stack Overflow + dev.to + Juejin）

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
