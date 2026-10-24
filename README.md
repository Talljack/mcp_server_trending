# MCP Server Trending

<div align="center">

**🎯 一站式独立开发者热门榜单聚合服务**

[![LightNow capabilities](https://lightnow.ai/badge/io.github.Talljack/mcp_server_trending)](https://lightnow.ai/servers/io.github.Talljack/mcp_server_trending)
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
- 💼 **We Work Remotely** - 全球最大远程工作社区
- 🦞 **Lobsters** - 高质量技术社区（类似 Hacker News）
- 📜 **Echo JS** - JavaScript 和前端新闻社区
- 🔌 **WordPress Plugins** - WordPress 插件目录
- 📄 **arXiv Papers** - 科研论文预印本平台
- 🎓 **Semantic Scholar** - AI 驱动的学术搜索引擎
- 🏆 **OpenReview** - ML 会议论文评审平台
- 📚 **Papers with Code** - ML/AI 研究论文（via HuggingFace Daily Papers）
- 🔄 **AlternativeTo** - 软件替代品推荐
- 🤖 **Replicate** - AI 模型 API 平台
- 🚀 **Betalist** - 早期创业项目发现
- 🐦 **Twitter/X** - 技术圈热门推文（via Nitter）
- 🛒 **Gumroad** - 数字产品销售平台热门产品
- 🔬 **Aggregation Analysis** - 跨平台聚合分析工具

> 专为独立开发者、Indie Hackers 和技术创业者设计

---

## ⚡ 快速开始

> **📌 重要说明**：本项目是 **stdio 模式** 的 MCP 服务器，需要在本地安装使用。不是云服务，而是本地工具。

### 方式一：从 PyPI 安装（推荐 ⭐）

> ⚠️ **重要提示**：
> - **Windows**：安装后可直接使用 `"command": "mcp-server-trending"`
> - **macOS/Linux**：需要创建符号链接或使用绝对路径（见下方步骤）

**推荐使用 pipx**（跨平台支持）：

<details>
<summary><b>🍎 macOS 安装步骤</b></summary>

```bash
# 1. 安装 pipx
brew install pipx
pipx ensurepath

# 2. 安装 mcp-server-trending
pipx install mcp-server-trending

# 3. 创建系统符号链接（重要！让 Cursor 等 GUI 应用能找到命令）
sudo ln -sf ~/.local/pipx/venvs/mcp-server-trending/bin/mcp-server-trending /usr/local/bin/mcp-server-trending

# 4. 验证
which mcp-server-trending  # 应该显示：/usr/local/bin/mcp-server-trending
```

完成后，配置文件中可以直接使用：
```json
{
  "command": "mcp-server-trending"
}
```

</details>

<details>
<summary><b>🐧 Linux 安装步骤</b></summary>

> ⚠️ **Python 版本要求**：本项目需要 **Python 3.10+**。如果你的系统默认是 Python 3.8/3.9，请先安装更高版本的 Python。

**检查 Python 版本**：
```bash
python3 --version
# 如果显示 Python 3.8.x 或 3.9.x，需要先安装 Python 3.10+
```

**安装 Python 3.10+（如果需要）**：
```bash
# Ubuntu 20.04/22.04:
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev

# 或使用 deadsnakes PPA（推荐，可获取最新版本）:
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# CentOS/RHEL/Rocky Linux:
sudo dnf install python3.11 python3.11-pip

# Arch Linux:
sudo pacman -S python  # Arch 通常已有最新版本
```

**安装步骤**：
```bash
# 1. 安装 pipx（使用 Python 3.10+）
# Ubuntu/Debian:
sudo apt install pipx
# 或使用指定版本的 pip:
python3.11 -m pip install --user pipx

# 2. 配置 PATH
pipx ensurepath

# 3. 安装 mcp-server-trending（指定 Python 版本）
pipx install mcp-server-trending --python python3.11
# 或者如果系统默认 python3 已是 3.10+:
pipx install mcp-server-trending

# 4. 创建系统符号链接（重要！让 GUI 应用能找到命令）
sudo ln -sf ~/.local/pipx/venvs/mcp-server-trending/bin/mcp-server-trending /usr/local/bin/mcp-server-trending

# 5. 验证
which mcp-server-trending  # 应该显示：/usr/local/bin/mcp-server-trending
mcp-server-trending --version
```

完成后，配置文件中可以直接使用：
```json
{
  "command": "mcp-server-trending"
}
```

</details>

<details>
<summary><b>🪟 Windows 安装步骤</b></summary>

```powershell
# 1. 安装 pipx
python -m pip install --user pipx
python -m pipx ensurepath

# 2. 安装 mcp-server-trending
pipx install mcp-server-trending

# 3. 重启终端或注销重新登录
# Windows 会自动将命令添加到 PATH
```

完成后，配置文件中可以直接使用：
```json
{
  "command": "mcp-server-trending"
}
```

</details>

**或使用 pip**（需要配置虚拟环境）：
```bash
pip install mcp-server-trending
```

> **💡 为什么需要创建符号链接（macOS/Linux）？**
>
> GUI 应用（Cursor、Claude Desktop 等）启动时不会读取 shell 配置文件（`~/.zshrc`、`~/.bashrc`），
> 因此无法找到 `~/.local/bin` 中的命令。创建符号链接到 `/usr/local/bin` 可以解决这个问题。
>
> **如果不想创建符号链接**，也可以在配置中使用绝对路径（详见下方"配置 AI 客户端"部分）。

### 方式二：从源码安装

```bash
git clone https://github.com/Talljack/mcp_server_trending.git
cd mcp_server_trending
bash install.sh
```

**就这么简单！** 🎉 脚本会自动完成所有配置。

---

## 🤔 安装方式对比

不知道选哪个？看这里：

| 安装方式 | 难度 | 优点 | 缺点 | 推荐场景 |
|---------|------|------|------|---------|
| **方式一：PyPI (pipx)** | ⭐⭐ 简单 | • 标准 Python 安装<br>• 版本管理方便<br>• 稳定可靠 | • macOS/Linux 需额外配置<br>• 需手动写配置文件 | 🎯 **所有用户推荐** |
| **方式二：源码** | ⭐⭐⭐ 中等 | • 可修改源码<br>• 最新功能<br>• 开发调试 | • 需要 git<br>• 配置较复杂 | 贡献者、开发者 |

**快速选择指南**：
- 🚀 **只想快速使用**？→ 方式一（PyPI + pipx）
- 💻 **想贡献代码或使用最新功能**？→ 方式二（源码）

---

## ❓ 关于 Smithery

**📍 在 Smithery 上找到我们**：[smithery.ai/server/@Talljack/mcp_server_trending](https://smithery.ai/server/@Talljack/mcp_server_trending)

**为什么 Smithery 页面显示 "No capabilities" 和 "No deployments"？**

本项目是 **stdio 模式** 的 MCP 服务器，而 Smithery 的托管部署主要支持 **HTTP/SSE 模式**。

- **stdio 模式**：本地安装，通过标准输入/输出通信（适合桌面客户端）✅
- **HTTP/SSE 模式**：云端托管，通过 HTTP 通信（适合 Web 应用）

**我们的选择**：
- ✅ 保持 stdio 模式 = 零成本 + 零运维 + 更安全 + 更快响应
- ❌ 切换到 HTTP 模式 = 需要云服务器 + 运维成本 + 复杂度增加

**Smithery 的作用**：
- 🔍 **发现平台** - 让用户找到我们的项目
- 📚 **文档入口** - 引导到 GitHub 查看完整文档
- ⚠️ **不是托管平台** - 需要本地安装使用

**如何安装**：
请使用上面的 **方式一（PyPI）** 或 **方式二（源码）** 安装，只需几分钟即可完成！

> 💡 **提示**：虽然不支持 Smithery 托管，但我们提供了详细的安装文档和配置示例，安装过程同样简单！

**功能列表**：
- ✅ 57+ MCP 工具
- ✅ 支持 27+ 平台（GitHub、Hacker News、Product Hunt、Twitter/X、Gumroad、Papers with Code 等）
- ✅ 跨平台聚合分析
- ✅ 智能缓存机制
- ✅ 完全免费开源

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

**方式 1：使用命令名（推荐 ✅）**

如果你按照上面的安装步骤创建了系统符号链接，可以直接使用命令名：

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

**方式 2：使用绝对路径（备选方案）**

如果你没有创建符号链接，或者方式 1 不工作，使用绝对路径：

```json
{
  "mcpServers": {
    "trending": {
      "command": "/Users/YOUR_USERNAME/.local/pipx/venvs/mcp-server-trending/bin/mcp-server-trending",
      "args": [],
      "env": {
        "HUGGINGFACE_TOKEN": "your_huggingface_token",
        "GITHUB_TOKEN": "your_github_token"
      }
    }
  }
}
```

**路径参考：**
- **macOS/Linux (pipx)**：`~/.local/pipx/venvs/mcp-server-trending/bin/mcp-server-trending`
- **Windows (pipx)**：`C:\Users\YOUR_USERNAME\.local\pipx\venvs\mcp-server-trending\Scripts\mcp-server-trending.exe`
- **源码安装**：`/path/to/mcp_server_trending/.venv/bin/mcp-server-trending`

> **💡 提示**：在终端运行 `which mcp-server-trending`（Windows: `where mcp-server-trending`）可以找到实际路径

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

**跨平台搜索示例（NEW 🌐）：**

```
在所有平台搜索关于 "AI agents" 的热门内容
```

```
今天有什么热门的技术内容？给我一个摘要
```

```
帮我在 GitHub、Hacker News 和 dev.to 上搜索 "rust" 相关内容
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
| **We Work Remotely** | 远程工作职位 | ✅ 完全可用 | ❌ 不需要 |
| **Lobsters** | 技术社区 | ✅ 完全可用 | ❌ 不需要 |
| **Echo JS** | JavaScript 新闻 | ✅ 完全可用 | ❌ 不需要 |
| **WordPress Plugins** | WordPress 插件 | ✅ 完全可用 | ❌ 不需要 |
| **arXiv Papers** | 科研论文预印本 | ✅ 完全可用 | ❌ 不需要 |
| **Semantic Scholar** | 学术搜索引擎 | ✅ 完全可用 | ❌ 不需要 |
| **OpenReview** | ML 会议论文评审 | ✅ 完全可用 | ❌ 不需要 |
| **Papers with Code** | ML/AI 研究论文 | ✅ 完全可用 | ❌ 不需要 |
| **AlternativeTo** | 软件替代品 | ✅ 精选数据 | ❌ 不需要 |
| **Replicate** | AI 模型平台 | ✅ 完全可用 | ❌ 不需要 |
| **Betalist** | 早期创业项目 | ✅ 完全可用 | ❌ 不需要 |
| **Twitter/X** | 技术圈推文 | ✅ 完全可用* | ❌ 不需要 |
| **Gumroad** | 数字产品平台 | ✅ 完全可用 | ❌ 不需要 |

> \* **说明**：
> - Product Hunt 需要配置 API credentials 才能获取真实数据，否则返回占位数据和配置指引
> - OpenRouter 需要配置 API Key 才能使用，未配置时返回错误提示和配置说明
> - **RemoteOK** 使用官方公开 JSON API (`https://remoteok.com/api`)，完全免费无需认证
>   - ✅ API 格式：第一条是表头，职位数据从第二条开始
>   - ⚠️ 网络要求：RemoteOK 会阻止 VPN/代理访问，如遇到 "Disable your VPN" 错误：
>     - 关闭 VPN 或代理软件
>     - 使用非数据中心 IP（家庭网络、手机热点等）
>     - 代码已实现智能降级：API 失败时自动尝试网页抓取
> - **Twitter/X** 通过 Nitter（开源 Twitter 前端）获取公开推文，无需 API Key
>   - ✅ 完全免费，无需认证
>   - ⚠️ Nitter 实例可能不稳定，代码已实现多实例自动切换
>   - 支持按标签、用户、聚合技术推文等多种查询方式

### 可用工具 (57个)

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

**We Work Remotely** (1个) 💼
- `get_weworkremotely_jobs` - 获取远程工作职位（支持多种分类：programming, design, devops 等）

**Lobsters** (3个) 🦞
- `get_lobsters_hottest` - 获取最热门的技术文章
- `get_lobsters_newest` - 获取最新的技术文章
- `get_lobsters_by_tag` - 按标签筛选文章（python, javascript, ai, rust 等）

**Echo JS** (2个) 📜
- `get_echojs_latest` - 获取最新 JavaScript 新闻
- `get_echojs_top` - 获取热门 JavaScript 新闻

**WordPress Plugins** (1个) 🔌
- `get_wordpress_plugins` - 获取 WordPress 插件目录热门插件

**Research Papers** (6个) 📄
- `get_arxiv_papers` - 获取 arXiv 科研论文（支持分类、关键词搜索）
- `search_semantic_scholar` - 搜索 Semantic Scholar 学术论文（AI 驱动、引用指标）
- `get_openreview_papers` - 获取 OpenReview ML 会议论文（ICLR、NeurIPS、ICML 等）
- `get_paperswithcode_trending` - 获取热门 ML/AI 研究论文
- `get_paperswithcode_latest` - 获取最新 ML/AI 研究论文
- `search_paperswithcode` - 搜索 ML/AI 研究论文（transformer、diffusion、llm 等）

**AlternativeTo** (2个) 🔄
- `get_alternativeto_trending` - 获取热门软件替代品（按平台筛选）
- `search_alternativeto` - 搜索特定软件的替代品（如 photoshop、slack）

**Replicate** (2个) 🤖
- `get_replicate_trending` - 获取热门 AI 模型
- `get_replicate_collection` - 获取特定类别 AI 模型（text-to-image、language-models 等）

**Betalist** (3个) 🚀
- `get_betalist_featured` - 获取精选早期创业项目
- `get_betalist_latest` - 获取最新早期创业项目
- `get_betalist_by_topic` - 按主题获取创业项目（ai、saas、fintech 等）

**Twitter/X** (5个) 🐦
- `get_twitter_hashtag_tweets` - 按标签获取推文（#buildinpublic、#indiehackers 等）
- `get_twitter_user_tweets` - 获取指定用户的推文
- `get_twitter_tech_tweets` - 获取聚合技术推文（多标签）
- `get_twitter_indie_hackers` - 获取知名独立开发者的推文
- `get_twitter_user_profile` - 获取用户资料信息

**Gumroad** (5个) 🛒
- `get_gumroad_discover` - 获取 Gumroad 热门/精选数字产品
- `get_gumroad_programming` - 获取编程相关产品（代码、教程、课程）
- `get_gumroad_design` - 获取设计相关产品（模板、素材、UI 套件）
- `search_gumroad` - 搜索 Gumroad 产品
- `get_gumroad_creator` - 获取指定创作者的产品列表

**Aggregation Analysis** (3个) 🔬
- `analyze_tech_stack` - 跨平台技术栈分析（GitHub + npm + PyPI + Stack Overflow + VS Code + Jobs）
- `get_indie_revenue_dashboard` - 独立开发者收入仪表板（Indie Hackers + TrustMRR）
- `track_topic_trends` - 话题趋势追踪（Hacker News + GitHub + Stack Overflow + dev.to + Juejin）

**Cross-Platform Search** (2个) 🌐 **NEW**
- `search_trending_all` - 跨平台搜索（在 GitHub、Hacker News、Product Hunt、dev.to、Lobsters、HuggingFace 等 15+ 平台中搜索）
- `get_trending_summary` - 今日热门摘要（汇总各平台 Top 内容，生成每日 Digest）

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

## 🐛 疑难解答

<details>
<summary><b>❌ Linux 上安装失败：Python 版本不兼容</b></summary>

**问题**：安装时报错 `requires-python>=3.10` 或运行时出现语法错误

**原因**：本项目需要 **Python 3.10+**，但很多 Linux 发行版默认的 Python 版本较低：
- Ubuntu 20.04 默认 Python 3.8
- Ubuntu 22.04 默认 Python 3.10 ✅
- CentOS 7/8 默认 Python 3.6/3.8
- Debian 11 默认 Python 3.9

**解决方案**：

**方案 1：安装更高版本的 Python**
```bash
# Ubuntu 20.04（使用 deadsnakes PPA）
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# CentOS/RHEL/Rocky Linux
sudo dnf install python3.11 python3.11-pip

# 然后使用指定版本安装
pipx install mcp-server-trending --python python3.11
```

**方案 2：使用 pyenv 管理多版本 Python**
```bash
# 安装 pyenv
curl https://pyenv.run | bash

# 添加到 shell 配置
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

# 安装 Python 3.11
pyenv install 3.11.0
pyenv global 3.11.0

# 然后正常安装
pipx install mcp-server-trending
```

**方案 3：使用 Docker**
```bash
docker run -it python:3.11-slim bash
pip install mcp-server-trending
```

</details>

<details>
<summary><b>❌ Cursor 报错：spawn mcp-server-trending ENOENT</b></summary>

**问题**：Cursor 找不到 `mcp-server-trending` 命令

**原因**：macOS/Linux 上的 GUI 应用无法读取用户 shell 配置（`~/.zshrc`、`~/.bashrc`），因此找不到 `~/.local/bin` 中的命令

**解决方案（二选一）**：

**方案 1：创建系统符号链接**（推荐）
```bash
# macOS/Linux
sudo ln -sf ~/.local/pipx/venvs/mcp-server-trending/bin/mcp-server-trending /usr/local/bin/mcp-server-trending
```

**方案 2：使用绝对路径**
在配置文件中使用完整路径：
```json
{
  "command": "/Users/YOUR_USERNAME/.local/pipx/venvs/mcp-server-trending/bin/mcp-server-trending"
}
```

找到实际路径：
```bash
# macOS/Linux
which mcp-server-trending
ls -la ~/.local/bin/mcp-server-trending

# Windows
where mcp-server-trending
```

</details>

<details>
<summary><b>🔍 如何验证安装是否成功？</b></summary>

```bash
# 检查命令是否存在
which mcp-server-trending  # macOS/Linux
where mcp-server-trending  # Windows

# 检查版本
mcp-server-trending --version

# 应该输出：mcp-server-trending 0.1.x
```

</details>

<details>
<summary><b>🪟 Windows 上 pipx 安装后找不到命令？</b></summary>

1. 运行 `pipx ensurepath`
2. 重启终端或注销重新登录
3. 验证 PATH：`echo %PATH%` 应该包含 `C:\Users\YourUsername\.local\bin`

</details>

<details>
<summary><b>🍎 macOS 上需要 sudo 密码，不想创建系统链接？</b></summary>

你可以直接在配置中使用绝对路径，不需要 sudo：

```json
{
  "command": "/Users/YOUR_USERNAME/.local/pipx/venvs/mcp-server-trending/bin/mcp-server-trending"
}
```

用你的实际用户名替换 `YOUR_USERNAME`。

</details>

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