# 如何将 mcp-server-trending 发布到 Smithery

## 背景

Smithery 是一个 MCP 服务器管理平台，可以让用户通过一条命令安装和配置 MCP 服务器。

## 前提条件

1. ✅ 包已发布到 PyPI（`mcp-server-trending` v0.1.3）
2. ✅ GitHub 仓库公开可访问（https://github.com/Talljack/mcp_server_trending）
3. ✅ README 包含详细的安装和配置说明
4. ✅ 代码已推送到 main 分支并打上 tag（v0.1.3）

## 🚀 快速发布步骤（推荐）

### 步骤 1：注册并获取 API Key

1. 访问 Smithery 官网：
   ```bash
   open https://smithery.ai/
   ```

2. 注册/登录账号

3. 获取 API Key：
   ```bash
   open https://smithery.ai/account/api-keys
   ```

   点击 "Create API Key" 创建一个新的 API key

### 步骤 2：通过 Smithery CLI 发布

```bash
# 1. 使用 API key 登录（交互式）
npx -y @smithery/cli login

# 或者直接使用 API key
export SMITHERY_API_KEY="your_api_key_here"

# 2. 搜索确认包是否已存在
npx -y @smithery/cli search mcp-server-trending

# 3. 如果 CLI 支持 publish 命令
npx -y @smithery/cli publish

# 4. 如果不支持，可能需要通过网站提交
```

### 步骤 3：验证发布

发布成功后，测试安装：

```bash
# 测试安装到 Cursor
npx -y @smithery/cli install mcp-server-trending --client cursor

# 或测试其他客户端
npx -y @smithery/cli install mcp-server-trending --client claude-desktop
```

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

1. **立即执行**：
   ```bash
   # 打开 Smithery 网站获取 API key
   open https://smithery.ai/account/api-keys
   ```

2. **获取 API key 后**：
   ```bash
   # 登录并尝试发布
   npx -y @smithery/cli login
   ```

3. **发布成功后**：
   - 更新 README.md，将 Smithery 安装方式标记为"推荐"
   - 在项目首页添加 Smithery 徽章
   - 发布 Release Notes 宣布支持 Smithery

---

**状态**：⏳ 待发布（需要 Smithery API key）

**更新日期**：2025-12-01

**维护者**：@Talljack

