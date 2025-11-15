# MCP Server Trending - 项目结构

## 📂 目录结构

```
mcp_server_trending/
├── 📄 配置文件
│   ├── pyproject.toml              # 项目配置 (支持 uv/pip)
│   ├── requirements.txt            # Python 依赖
│   ├── .env.example                # 环境变量模板
│   ├── .gitignore                  # Git 忽略文件
│   └── LICENSE                     # MIT 许可证
│
├── 📚 文档
│   ├── README.md                   # 项目介绍
│   ├── PRD.md                      # 产品需求文档
│   ├── QUICKSTART.md               # 快速开始指南
│   ├── CONTRIBUTING.md             # 贡献指南
│   ├── IMPLEMENTATION_SUMMARY.md   # 实现总结
│   ├── INSTALL_SUCCESS.md          # 安装成功指南
│   └── PROJECT_STRUCTURE.md        # 本文件
│
├── 💻 源代码 (src/)
│   ├── models/                     # 数据模型
│   │   ├── __init__.py
│   │   ├── base.py                 # BaseModel, TrendingResponse
│   │   ├── github.py               # GitHubRepository, GitHubDeveloper
│   │   ├── hackernews.py           # HackerNewsStory
│   │   └── producthunt.py          # ProductHuntProduct
│   │
│   ├── fetchers/                   # 数据获取器
│   │   ├── __init__.py
│   │   ├── base.py                 # BaseFetcher (抽象基类)
│   │   ├── github/
│   │   │   ├── __init__.py
│   │   │   └── fetcher.py          # GitHubTrendingFetcher
│   │   ├── hackernews/
│   │   │   ├── __init__.py
│   │   │   └── fetcher.py          # HackerNewsFetcher
│   │   └── producthunt/
│   │       ├── __init__.py
│   │       └── fetcher.py          # ProductHuntFetcher
│   │
│   ├── utils/                      # 工具类
│   │   ├── __init__.py
│   │   ├── cache.py                # SimpleCache (内存缓存)
│   │   ├── http_client.py          # HTTPClient (带重试的 HTTP 客户端)
│   │   └── logger.py               # 日志工具
│   │
│   ├── tools/                      # MCP Tools (预留)
│   │   └── (未来扩展)
│   │
│   ├── __init__.py                 # 包初始化
│   ├── config.py                   # 配置管理
│   └── server.py                   # MCP Server 主入口 ⭐
│
├── 🧪 测试 (tests/)
│   ├── __init__.py
│   ├── conftest.py                 # pytest 配置
│   ├── test_cache.py               # 缓存测试
│   ├── test_models.py              # 模型测试
│   ├── test_integration.py         # 集成测试
│   └── test_server_setup.py        # 服务器设置测试
│
├── 📖 示例 (examples/)
│   └── basic_usage.py              # 基本使用示例
│
└── 🔧 虚拟环境
    └── .venv/                      # Python 虚拟环境 (使用 uv 创建)
```

## 📊 文件统计

- **总文件数**: 32 个
- **Python 文件**: 26 个
- **文档文件**: 7 个
- **代码行数**: ~2500+ 行

## 🏗️ 架构设计

### 分层架构

```
┌─────────────────────────────────┐
│   MCP Server (server.py)        │  ← MCP 协议层
├─────────────────────────────────┤
│   Tools Layer                   │  ← 工具注册层
├─────────────────────────────────┤
│   Fetchers (GitHub, HN, PH)     │  ← 数据获取层
├─────────────────────────────────┤
│   Utils (HTTP, Cache, Logger)   │  ← 基础设施层
├─────────────────────────────────┤
│   Models (Data Structures)      │  ← 数据模型层
└─────────────────────────────────┘
```

### 数据流

```
Claude Desktop
    ↓ (stdio)
MCP Server
    ↓ (tool call)
Fetcher
    ↓ (check cache)
Cache (miss) → HTTP Client → External API
    ↓ (parse & model)
TrendingResponse
    ↓ (serialize)
JSON Response → Claude Desktop
```

## 🔑 核心组件

### 1. BaseFetcher (src/fetchers/base.py)

抽象基类，提供：
- ✅ 统一的缓存管理
- ✅ HTTP 请求封装
- ✅ 错误处理
- ✅ 响应格式化

### 2. HTTPClient (src/utils/http_client.py)

HTTP 客户端，特性：
- ✅ 自动重试机制
- ✅ 速率限制
- ✅ 超时控制
- ✅ 异步支持

### 3. SimpleCache (src/utils/cache.py)

内存缓存，功能：
- ✅ TTL 支持
- ✅ 过期清理
- ✅ 缓存统计

### 4. TrendingMCPServer (src/server.py)

MCP Server 实现：
- ✅ 4 个 MCP Tools
- ✅ 3 个平台集成
- ✅ stdio 通信

## 📝 命名规范

### Python 文件
- **模块**: `snake_case` (例如: `http_client.py`)
- **类**: `PascalCase` (例如: `GitHubTrendingFetcher`)
- **函数**: `snake_case` (例如: `fetch_trending_repos`)
- **常量**: `UPPER_CASE` (例如: `BASE_URL`)

### 目录结构
- **平台文件夹**: `lowercase` (例如: `github/`, `hackernews/`)
- **功能文件夹**: `lowercase` (例如: `models/`, `fetchers/`)

## 🚀 扩展指南

### 添加新平台 (例如: Reddit)

1. **创建数据模型**
   ```bash
   src/models/reddit.py
   ```

2. **实现 Fetcher**
   ```bash
   src/fetchers/reddit/
   ├── __init__.py
   └── fetcher.py
   ```

3. **注册 MCP Tool**
   在 `src/server.py` 中添加

4. **编写测试**
   ```bash
   tests/test_reddit.py
   ```

5. **更新文档**
   - README.md
   - PRD.md

## 📦 依赖关系

```
mcp >= 1.0.0           # MCP SDK
httpx >= 0.27.0        # 异步 HTTP 客户端
beautifulsoup4 >= 4.12 # HTML 解析
```

## 🔧 开发工具 (可选)

```
pytest >= 7.0.0        # 测试框架
pytest-asyncio >= 0.21 # 异步测试
black >= 23.0.0        # 代码格式化
ruff >= 0.1.0          # Linting
mypy >= 1.0.0          # 类型检查
```

---

**项目状态**: ✅ Phase 1 完成，可用于生产环境
**最后更新**: 2025-11-15
