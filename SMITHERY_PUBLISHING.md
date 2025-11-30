# 发布到 Smithery 注册表

本文档说明如何将 `mcp-server-trending` 发布到 Smithery 注册表，让更多用户可以通过 Smithery 发现和安装。

## 📋 前置要求

- ✅ 已发布到 PyPI（当前版本：0.1.2）
- ✅ 已创建 `smithery.json` 配置文件
- ✅ GitHub 仓库公开且文档完善

## 🚀 发布步骤

### 方法 1：通过 Smithery CLI（推荐）

#### 1. 安装 Smithery CLI

```bash
npm install -g @smithery/cli
```

#### 2. 登录 Smithery（如需要）

```bash
smithery login
```

#### 3. 发布到 Smithery

在项目根目录运行：

```bash
smithery publish
```

该命令会：
- ✅ 读取 `smithery.json` 配置
- ✅ 验证包信息
- ✅ 发布到 Smithery 注册表

---

### 方法 2：通过 GitHub Pull Request

如果 Smithery 使用 GitHub 仓库管理注册表，可以：

#### 1. Fork Smithery 注册表仓库

```bash
# 假设注册表在 https://github.com/smithery/registry
git clone https://github.com/smithery/registry
cd registry
```

#### 2. 添加你的包信息

在注册表中添加 `mcp-server-trending` 的配置（通常是添加一个 JSON 文件）

#### 3. 提交 Pull Request

```bash
git checkout -b add-mcp-server-trending
git add .
git commit -m "Add mcp-server-trending to registry"
git push origin add-mcp-server-trending
# 然后在 GitHub 上创建 Pull Request
```

---

### 方法 3：通过 Smithery 网站

1. 访问 https://smithery.ai
2. 注册/登录开发者账户
3. 点击 "Submit MCP Server" 或类似按钮
4. 填写表单：
   - Package Name: `mcp-server-trending`
   - Package Manager: `pipx`
   - Repository URL: `https://github.com/Talljack/mcp_server_trending`
   - Description: "MCP Server for trending data from multiple platforms..."
5. 提交审核

---

## 📝 smithery.json 配置说明

当前配置文件内容：

```json
{
  "name": "mcp-server-trending",
  "version": "0.1.2",
  "description": "MCP Server for trending data from multiple platforms for indie developers",
  "author": "MCP Server Trending Team",
  "repository": "https://github.com/Talljack/mcp_server_trending",
  "license": "MIT",
  "type": "python",
  "install": {
    "pipx": "mcp-server-trending"
  },
  "categories": [
    "data",
    "trending",
    "developer-tools",
    "indie-hackers"
  ],
  "keywords": [
    "mcp",
    "trending",
    "github",
    "hackernews",
    "producthunt",
    "indie-hackers"
  ]
}
```

### 字段说明：

- **name**: 包名，需与 PyPI 包名一致
- **version**: 版本号，需与 PyPI 版本一致
- **description**: 简短描述
- **type**: `"python"` 表示 Python 包
- **install.pipx**: PyPI 包名
- **categories**: 帮助用户分类查找
- **keywords**: 搜索关键词

---

## ✅ 发布后的好处

发布到 Smithery 后：

1. **增加曝光度**
   - 用户可以在 https://smithery.ai 上搜索到你的包
   - 出现在相关分类和推荐中

2. **简化安装**
   - 用户可以一键安装：
   ```bash
   npx @smithery/cli install mcp-server-trending --client cursor
   ```

3. **统一管理**
   - 用户可以通过 Smithery 管理多个 MCP 服务器
   - 自动更新和版本管理

---

## 🔄 更新已发布的包

当你发布新版本到 PyPI 后：

### 1. 更新 smithery.json

```json
{
  "version": "0.1.3"  // 更新版本号
}
```

### 2. 重新发布

```bash
smithery publish
```

或者 Smithery 可能会自动检测 PyPI 的更新。

---

## 🐛 常见问题

### Q: 是否必须发布到 Smithery？
**A**: 不是必须的。用户仍然可以通过 PyPI 安装：
```bash
pipx install mcp-server-trending
```
发布到 Smithery 只是增加了一个分发渠道。

### Q: Smithery 如何知道使用 pipx？
**A**:
1. 通过包名格式识别（不以 `@` 开头 = Python 包）
2. 通过 `smithery.json` 中的 `type: "python"` 配置
3. 通过检测 PyPI 上是否有该包

### Q: 发布需要多久审核？
**A**: 通常 1-3 个工作日（具体取决于 Smithery 团队）

---

## 📚 相关资源

- Smithery 官网: https://smithery.ai
- Smithery CLI: https://www.npmjs.com/package/@smithery/cli
- MCP 协议: https://modelcontextprotocol.io

---

## 💡 下一步

1. 确认 Smithery 的具体发布流程（查看官方文档）
2. 选择合适的发布方法（CLI 或 PR）
3. 提交发布申请
4. 等待审核通过
5. 在 README 中添加 Smithery 徽章 🎉

---

**注意**: Smithery 的具体发布流程可能会变化，请以官方最新文档为准。

