# MCP Server Trending

<div align="center">

**一站式独立开发者热门榜单聚合服务**

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](#) | [中文文档](#)

</div>

## 🌟 项目简介

MCP Server Trending 是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的热门榜单聚合服务，专为独立开发者、Indie Hackers 和技术创业者设计。通过统一的 MCP 接口，让 AI 助手能够轻松查询和分析来自多个平台的热门内容。

### Phase 1 支持的平台

- ✅ **GitHub Trending** - 热门仓库和开发者
- ✅ **Hacker News** - 技术社区热门故事
- ✅ **Product Hunt** - 热门产品发布

## 🚀 快速开始

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/yourusername/mcp_server_trending.git
cd mcp_server_trending

# 安装依赖
pip install -r requirements.txt
```

### 配置环境变量（可选）

```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的 API keys
# 注意: GitHub 和 Product Hunt 的 API keys 是可选的
```

### 运行服务器

```bash
# 直接运行
python -m src.mcp_server_trending.server

# 或者作为模块运行
python src/mcp_server_trending/server.py
```

### 集成到 Claude Desktop

在你的 Claude Desktop 配置文件中添加：

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "trending": {
      "command": "python",
      "args": [
        "/path/to/mcp_server_trending/src/mcp_server_trending/server.py"
      ]
    }
  }
}
```

## 📚 使用示例

### GitHub Trending

```python
# 获取 Python 每日热门仓库
get_github_trending_repos(
    time_range="daily",
    language="python"
)

# 获取本周热门开发者
get_github_trending_developers(
    time_range="weekly",
    language="go"
)
```

### Hacker News

```python
# 获取 Top Stories
get_hackernews_stories(
    story_type="top",
    limit=30
)

# 获取 Show HN
get_hackernews_stories(
    story_type="show",
    limit=20
)
```

### Product Hunt

```python
# 获取今日产品
get_producthunt_products(
    time_range="today"
)

# 按主题筛选
get_producthunt_products(
    time_range="week",
    topic="Developer Tools"
)
```

## 🏗️ 项目架构

```
mcp_server_trending/
├── src/
│   └── mcp_server_trending/
│       ├── models/              # 数据模型（类型定义）
│       │   ├── base.py          # 基础模型
│       │   ├── github.py        # GitHub 数据模型
│       │   ├── producthunt.py   # Product Hunt 数据模型
│       │   └── hackernews.py    # Hacker News 数据模型
│       ├── fetchers/            # 数据获取层（按平台分文件夹）
│       │   ├── base.py          # BaseFetcher 抽象类
│       │   ├── github/          # GitHub fetcher
│       │   ├── producthunt/     # Product Hunt fetcher
│       │   └── hackernews/      # Hacker News fetcher
│       ├── utils/               # 工具函数
│       │   ├── logger.py        # 日志工具
│       │   ├── http_client.py   # HTTP 客户端
│       │   └── cache.py         # 缓存管理
│       ├── config.py            # 配置管理
│       └── server.py            # MCP Server 主入口
├── tests/                       # 测试文件
├── requirements.txt             # 依赖列表
├── .env.example                 # 环境变量模板
├── README.md                    # 项目文档
└── PRD.md                       # 产品需求文档
```

## 🎯 设计特点

### 高复用性架构

- **BaseFetcher** 抽象类：提供通用的缓存、HTTP 请求、错误处理
- **BaseModel** 数据模型：统一的数据序列化和转换
- **HTTPClient** 工具类：带重试机制和速率限制的 HTTP 客户端
- **SimpleCache** 缓存系统：简单高效的内存缓存

### 类型安全

- 全面使用 Python Type Hints
- 严格的数据模型定义
- 类型检查友好

### 模块化设计

- 每个平台独立的文件夹
- 清晰的职责分离
- 易于添加新平台

## 🔧 开发指南

### 添加新平台

1. **创建数据模型** - 在 `models/` 下创建新的模型文件
2. **实现 Fetcher** - 在 `fetchers/` 下创建新的文件夹和 fetcher
3. **注册 MCP Tool** - 在 `server.py` 中注册新的工具
4. **更新文档** - 更新 README 和 PRD

### 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_github.py
```

## 📝 数据格式

所有 API 返回统一的 `TrendingResponse` 格式：

```json
{
  "success": true,
  "platform": "github",
  "data_type": "trending_repos",
  "timestamp": "2025-11-15T10:30:00Z",
  "cache_hit": false,
  "data": [
    {
      "rank": 1,
      "name": "...",
      "url": "...",
      ...
    }
  ],
  "metadata": {
    "total_count": 25,
    "time_range": "daily"
  }
}
```

## 🤝 贡献指南

欢迎贡献！请查看我们的贡献指南：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [mcp-github-trending](https://github.com/hetaoBackend/mcp-github-trending) - 参考实现

## 📮 联系方式

- 提交 Issue: [GitHub Issues](https://github.com/yourusername/mcp_server_trending/issues)
- 讨论: [GitHub Discussions](https://github.com/yourusername/mcp_server_trending/discussions)

## 🗺️ Roadmap

查看 [PRD.md](PRD.md) 了解完整的产品规划。

### Phase 1 ✅ (当前)
- GitHub Trending
- Hacker News
- Product Hunt

### Phase 2 (计划中)
- Reddit 热门话题
- Indie Hackers
- DevHunt

### Phase 3 (计划中)
- OpenRouter LLM Rankings
- Hugging Face Trending
- 公开收入排名

---

**Star ⭐ 本项目以支持独立开发者社区！**
