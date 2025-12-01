# 如何将 mcp-server-trending 发布到 Smithery

## 背景

Smithery 是一个 MCP 服务器管理平台，可以让用户通过一条命令安装和配置 MCP 服务器。

## 前提条件

1. ✅ 包已发布到 PyPI（`mcp-server-trending` v0.1.3）
2. ✅ GitHub 仓库公开可访问（https://github.com/Talljack/mcp_server_trending）
3. ✅ README 包含详细的安装和配置说明
4. ✅ 代码已推送到 main 分支并打上 tag（v0.1.3）

## ⚠️ 当前状态

经过测试发现：

1. ❌ **Smithery CLI 不支持 `publish` 命令**
   ```bash
   npx -y @smithery/cli publish
   # error: unknown command 'publish'
   ```

2. ❌ **`search` 命令需要 API key 但无法正常工作**
   ```bash
   export SMITHERY_API_KEY="your_key"
   npx -y @smithery/cli search mcp-server-trending
   # Error: HTTP 401: Invalid API key
   ```

3. ✅ **CLI 支持的命令**：
   - `install` - 安装已存在的服务器
   - `uninstall` - 卸载服务器
   - `inspect` - 查看服务器信息
   - `run` - 运行服务器
   - `dev` - 开发模式
   - `build` - 构建服务器
   - `list` - 列出已安装的服务器
   - `search` - 搜索服务器（需要有效 API key）
   - `login` - 登录

## 🔍 发布方式调查

### 方式 1：通过 Smithery 网站提交（推荐尝试）

1. 访问 Smithery 网站：
   ```bash
   open https://smithery.ai/
   ```

2. 查找以下可能的入口：
   - "Submit Server" 按钮
   - "Add Server" 链接
   - "Publish" 菜单
   - 用户仪表板中的提交选项

3. 如果找到提交表单，填写包信息（见下方"包信息"部分）

### 方式 2：通过 GitHub（如果有 registry 仓库）

1. 访问 Smithery GitHub 组织：
   ```bash
   open https://github.com/smithery-ai
   ```

2. 查找是否有 `registry` 或 `servers` 仓库

3. 如果有，提交 PR 添加服务器配置

### 方式 3：联系 Smithery 支持团队

如果以上方式都不可行，可以通过以下渠道联系：

1. **邮件支持**：
   - 发送邮件到：support@smithery.ai（推测）
   - 或查看网站底部的联系方式

2. **GitHub Issue**：
   - 在 Smithery 的 GitHub 仓库提交 issue
   - 请求添加 `mcp-server-trending` 到 registry

3. **社区渠道**：
   - Discord（如果有）
   - Twitter/X: 搜索 @smithery 或 #smithery
   - 在 MCP 相关社区询问

## 📝 包信息（提交时可能需要）

如果 Smithery 要求填写包信息，可以使用以下内容：

```yaml
name: mcp-server-trending
type: python
package_name: mcp-server-trending
pypi_url: https://pypi.org/project/mcp-server-trending/
install_command: pipx install mcp-server-trending
command: mcp-server-trending
description: 🎯 一站式独立开发者热门榜单聚合服务 - 聚合 GitHub Trending、Hacker News、Product Hunt、Indie Hackers 等 29+ 平台的热门内容
repository: https://github.com/Talljack/mcp_server_trending
homepage: https://github.com/Talljack/mcp_server_trending
documentation: https://github.com/Talljack/mcp_server_trending/blob/main/README.md
author: Talljack
license: MIT
version: 0.1.3
tags:
  - trending
  - github
  - hackernews
  - product-hunt
  - indie-hackers
  - ai-tools
  - developer-tools
  - aggregation
platforms:
  - linux
  - macos
  - windows
categories:
  - productivity
  - developer-tools
  - data-aggregation
features:
  - 29+ 平台热门内容聚合
  - 45+ MCP 工具
  - GitHub Trending 仓库和开发者
  - Hacker News 热门故事
  - Indie Hackers 收入报告
  - AI 工具和模型排行
  - 远程工作机会
  - 学术论文搜索
  - 跨平台技术栈分析
```

## Smithery 如何识别 Python vs Node.js 包

Smithery 通过以下方式识别包类型：

1. **包名格式**：
   - `@scope/package-name` → Node.js 包（使用 npx）
   - `package-name` → Python 包（使用 pipx）

2. **安装命令**：
   - Node.js: `npx @scope/package-name`
   - Python: `pipx install package-name`

由于我们的包名是 `mcp-server-trending`（无 `@scope/`），Smithery 应该自动识别为 Python 包并使用 `pipx` 安装。

## 待确认信息

以下信息需要通过 Smithery 官方渠道确认：

1. ☑️ Smithery 是否有公开的 registry 仓库？
2. ☑️ 是否支持直接从 PyPI 拉取包？
3. ☑️ 是否需要手动提交包信息？
4. ☑️ 提交审核需要多长时间？

## 联系方式

- Smithery 官网：https://smithery.ai/
- Smithery 文档：https://smithery.ai/docs（如果有）
- API Keys：https://smithery.ai/account/api-keys

## 🔍 常见问题

### Q1: Smithery 如何识别这是 Python 包？

**A:** Smithery 通过包名格式识别：
- `@scope/package-name` → Node.js 包（使用 `npx`）
- `package-name` → Python 包（使用 `pipx`）

我们的包名是 `mcp-server-trending`（无 `@scope/`），所以会被识别为 Python 包。

### Q2: 需要在 npm 上发布吗？

**A:** 不需要。Smithery 支持直接从 PyPI 安装 Python 包。

### Q3: 发布后多久可以使用？

**A:** 通常发布后立即可用，但可能需要几分钟的审核时间。

### Q4: 如果 CLI 登录失败怎么办？

**A:** 可以尝试：
1. 通过网站界面提交
2. 联系 Smithery 支持：support@smithery.ai
3. 在 Smithery Discord/社区寻求帮助

## 📞 联系方式

- **Smithery 官网**：https://smithery.ai/
- **API Keys 管理**：https://smithery.ai/account/api-keys
- **文档**（如有）：https://smithery.ai/docs
- **支持邮箱**：support@smithery.ai

## ✅ 发布检查清单

发布前确认：

- [ ] PyPI 包已发布（v0.1.3）
- [ ] GitHub 仓库公开
- [ ] README 完整且清晰
- [ ] 已获取 Smithery API key
- [ ] 已测试 `pipx install mcp-server-trending` 可用
- [ ] 配置示例已添加到 README

发布后确认：

- [ ] 可以通过 `npx -y @smithery/cli search mcp-server-trending` 找到
- [ ] 可以通过 `npx -y @smithery/cli install mcp-server-trending --client cursor` 安装
- [ ] 安装后在 Cursor 中可以正常使用
- [ ] 更新 README 添加 Smithery 安装方式

## 🎯 下一步行动

### 立即可做的：

1. **浏览 Smithery 网站**：
   ```bash
   open https://smithery.ai/
   open https://smithery.ai/servers
   ```
   查找"Submit"、"Add Server"或"Publish"相关的入口

2. **检查 Smithery GitHub**：
   ```bash
   open https://github.com/smithery-ai
   ```
   查看是否有 registry 仓库或相关文档

3. **准备联系邮件**（如果需要）：
   ```
   主题：Request to Add mcp-server-trending to Smithery Registry
   
   内容：
   Hi Smithery Team,
   
   I would like to submit my MCP server to the Smithery registry:
   
   - Name: mcp-server-trending
   - Type: Python (PyPI)
   - PyPI: https://pypi.org/project/mcp-server-trending/
   - GitHub: https://github.com/Talljack/mcp_server_trending
   - Description: 🎯 一站式独立开发者热门榜单聚合服务
   - Version: 0.1.3
   - Install: pipx install mcp-server-trending
   
   The package is already published on PyPI and fully functional.
   Could you please guide me on how to add it to the Smithery registry?
   
   Thank you!
   ```

### 发布成功后：

- [ ] 更新 README.md，将 Smithery 安装方式标记为"推荐"
- [ ] 在项目首页添加 Smithery 徽章
- [ ] 发布 Release Notes 宣布支持 Smithery
- [ ] 更新本文档记录实际发布流程

---

## 📌 临时解决方案

在 Smithery 发布之前，用户可以使用以下方式安装：

### 方式 1：PyPI 安装（当前推荐）

```bash
# macOS/Linux
pipx install mcp-server-trending
sudo ln -sf ~/.local/pipx/venvs/mcp-server-trending/bin/mcp-server-trending /usr/local/bin/mcp-server-trending

# Windows
pipx install mcp-server-trending
```

然后在 `.cursor/mcp.json` 中配置：
```json
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending"
    }
  }
}
```

### 方式 2：源码安装

```bash
git clone https://github.com/Talljack/mcp_server_trending.git
cd mcp_server_trending
bash install.sh
```

---

**状态**：⏳ 待发布（正在寻找提交方式）

**更新日期**：2025-12-01

**维护者**：@Talljack

**问题**：Smithery CLI 不支持 `publish` 命令，需要找到正确的提交渠道

