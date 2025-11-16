# 包结构重构 - 实现类似 npx 的使用体验

## ✅ 完成的改进

### 1. 重构包结构

**之前的结构**:
```
src/
  server.py
  config.py
  models/
  fetchers/
  utils/
```

**现在的结构**:
```
src/
  mcp_server_trending/    ← 标准 Python 包
    __init__.py
    server.py
    config.py
    models/
    fetchers/
    utils/
```

### 2. 配置命令行入口

**pyproject.toml**:
```toml
[project.scripts]
mcp-server-trending = "mcp_server_trending.server:cli_main"
```

安装后会自动创建可执行命令：
```bash
.venv/bin/mcp-server-trending
```

### 3. 简化配置方式

#### 之前的配置（复杂）:
```json
{
  "command": "/absolute/path/.venv/bin/python",
  "args": ["/absolute/path/src/server.py"],
  "env": {
    "PYTHONPATH": "/absolute/path/src"
  }
}
```

#### 现在的配置（简单）:
```json
{
  "command": "mcp-server-trending"
}
```

或者从源码安装时：
```json
{
  "command": "/path/to/.venv/bin/mcp-server-trending"
}
```

---

## 🚀 使用方式对比

### Node.js MCP (npx)
```bash
# 全局安装
npm install -g @modelcontextprotocol/server-github

# 配置
{
  "command": "mcp-server-github"
}
```

### Python MCP - 改进后
```bash
# 未来从 PyPI 安装（需要先发布）
pip install mcp-server-trending

# 配置
{
  "command": "mcp-server-trending"
}
```

**体验几乎一致！** ✨

---

## 📋 改进对比

### 安装步骤

| 指标 | 之前 | 现在 |
|------|------|------|
| **克隆代码** | ✅ 必需 | ✅ 必需 (PyPI 发布后可选) |
| **创建虚拟环境** | ✅ 必需 | ✅ 必需 |
| **安装依赖** | ✅ 必需 | ✅ 必需 |
| **配置路径** | 😞 绝对路径 | ✅ 命令名称 |

### 配置复杂度

| 指标 | 之前 | 现在 |
|------|------|------|
| **配置字段** | 4个 (command, args, env, ...) | 1个 (command) |
| **需要知道路径** | ✅ 3个路径 | ✅ 1个路径 (仅源码安装) |
| **易于分享** | ❌ 每人路径不同 | ✅ 统一命令 |

### 未来 PyPI 发布后

| 指标 | Node.js (npm) | Python (PyPI) |
|------|---------------|---------------|
| **安装命令** | `npm install -g` | `pip install` |
| **配置方式** | 命令名称 | 命令名称 |
| **体验** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 下一步计划

### 1. 发布到 PyPI
```bash
# 构建
python -m build

# 上传到 PyPI
twine upload dist/*
```

### 2. 用户安装（发布后）
```bash
# 一行命令安装
pip install mcp-server-trending

# 配置
{
  "mcpServers": {
    "trending": {
      "command": "mcp-server-trending"
    }
  }
}
```

### 3. 自动发布
GitHub Release 时会自动发布到 PyPI（已配置 CI）

---

## 🔧 技术细节

### 1. 包结构
- 使用 `src/` layout（推荐的 Python 包结构）
- 通过 `setuptools.packages.find` 自动发现包

### 2. 入口点
```python
# src/mcp_server_trending/server.py
def cli_main():
    """CLI entry point."""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()
```

### 3. 相对导入
```python
# 使用相对导入
from .config import config
from .fetchers import GitHubTrendingFetcher
from .utils import SimpleCache
```

---

## ✨ 总结

现在 Python MCP Server 的使用体验已经和 Node.js 的 `npx` 一样简单！

**当前**: 从源码安装，需要指定完整路径
**未来**: 发布到 PyPI 后，一行命令安装，配置只需命令名称

这为用户提供了更好的体验，也让项目更专业和易用！🎉
