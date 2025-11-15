# Product Requirements Document (PRD)
# MCP Server Trending - 独立开发者热门榜单服务

## 项目概述

**项目名称**: MCP Server Trending
**目标用户**: 独立开发者、Indie Hackers、技术创业者
**项目定位**: 基于 Model Context Protocol (MCP) 的热门榜单聚合服务，为独立开发者提供一站式的行业动态、产品趋势和收入数据查询能力

## 1. 产品背景与目标

### 1.1 背景
独立开发者需要持续关注行业动态、技术趋势、热门产品和成功案例，但这些信息分散在多个平台上。通过 MCP Server 的方式，可以让 AI 助手直接帮助开发者查询和分析这些榜单数据，提高信息获取效率。

### 1.2 产品目标
- 聚合独立开发者最关心的多个平台的热门榜单
- 提供统一的查询接口，支持 AI 助手无缝集成
- 实时更新榜单数据，保证信息的时效性
- 支持多维度筛选和自定义查询条件

## 2. 核心功能模块

### 2.1 榜单资源列表

#### 2.1.1 技术开发类
1. **GitHub Trending**
   - Repositories Trending (按日/周/月)
   - Developers Trending (按日/周/月)
   - 支持按编程语言筛选
   - 支持按 Spoken Language 筛选

2. **DevHunt Rankings**
   - 每日最佳开发工具
   - 每周最佳开发工具
   - 月度最佳开发工具
   - 按分类筛选（CLI Tools, APIs, Libraries 等）

3. **Stack Overflow Trends**
   - 热门问题 (按周/月)
   - 上升最快的技术标签
   - 最活跃的开发者

#### 2.1.2 产品发布类
4. **Product Hunt**
   - 每日产品榜单 (Today, This Week, This Month)
   - 按分类筛选（Developer Tools, AI, SaaS 等)
   - Golden Kitty Awards 历史获奖产品
   - 即将发布的产品 (Upcoming)

5. **Hacker News**
   - Front Page (首页热门)
   - Best Stories (最佳故事)
   - Ask HN (问答)
   - Show HN (展示项目)
   - 支持按评分和评论数排序

#### 2.1.3 社区讨论类
6. **Reddit 热门话题**
   - r/SideProject
   - r/EntrepreneurRideAlong
   - r/Entrepreneur
   - r/startups
   - r/SaaS
   - r/webdev
   - r/programming
   - 支持按时间范围筛选 (今日/本周/本月/全年)

7. **Indie Hackers**
   - 热门帖子 (Popular Posts)
   - 收入报告 (Income Reports)
   - 项目里程碑 (Milestones)
   - 本周创业者

#### 2.1.4 收入与商业类
8. **Open Startup Rankings**
   - 按 MRR (月收入) 排名
   - 按增长率排名
   - 新加入的开源创业公司

9. **Stripe 收入排名** (通过公开数据)
   - Top earning indie projects (如果有公开 API 或爬虫)
   - MicroConf 分享的收入案例

10. **MicroSaaS Rankings**
    - MicroAcquire 上的热门项目
    - Acquire.com 上的交易数据

#### 2.1.5 AI 与 LLM 类
11. **OpenRouter Rankings**
    - 最受欢迎的 LLM 模型
    - 最佳性价比模型
    - 新上线的模型

12. **Hugging Face Trending**
    - 热门模型 (Models)
    - 热门数据集 (Datasets)
    - 热门 Spaces (应用)

13. **AI Tools Directory**
    - There's An AI For That (热门 AI 工具)
    - Future Tools (新上线的 AI 工具)

#### 2.1.6 设计与资源类
14. **Dribbble Trending**
    - 热门设计作品
    - 按分类筛选

15. **Behance Trending**
    - 热门创意项目

#### 2.1.7 开发者收入与案例
16. **BuildInPublic 案例**
    - Twitter/X 上的 #BuildInPublic 热门动态
    - 收入截图和里程碑分享

17. **Gumroad Top Creators**
    - 畅销创作者排行
    - 热门产品

18. **Awesome Lists**
    - Awesome GitHub 精选列表中的新增/热门项目

## 3. 技术架构

### 3.1 技术栈
- **开发语言**: Python 3.10+
- **核心框架**: MCP Python SDK
- **数据获取**:
  - 官方 API (GitHub API, Reddit API, etc.)
  - Web Scraping (BeautifulSoup4, Playwright)
  - RSS/Atom Feeds
- **缓存**: Redis (可选，用于减少 API 调用)
- **部署**: Docker + Docker Compose

### 3.2 MCP Server 架构

```
mcp-server-trending/
├── src/
│   ├── server.py              # MCP Server 主入口
│   ├── config.py              # 配置管理
│   ├── tools/                 # MCP Tools 定义
│   │   ├── __init__.py
│   │   ├── github_trending.py
│   │   ├── producthunt.py
│   │   ├── hackernews.py
│   │   ├── reddit.py
│   │   ├── devhunt.py
│   │   ├── indiehackers.py
│   │   ├── openrouter.py
│   │   ├── huggingface.py
│   │   └── ...
│   ├── fetchers/              # 数据获取层
│   │   ├── base.py
│   │   ├── api_fetcher.py
│   │   ├── scraper.py
│   │   └── ...
│   ├── cache/                 # 缓存管理
│   │   └── cache_manager.py
│   └── utils/                 # 工具函数
│       ├── logger.py
│       └── validators.py
├── tests/                     # 测试文件
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example               # 环境变量模板
├── requirements.txt
├── README.md
├── PRD.md
└── LICENSE
```

### 3.3 MCP Tools 设计

每个榜单对应一个或多个 MCP Tool，例如：

```python
# github_trending Tool
{
  "name": "get_github_trending_repos",
  "description": "获取 GitHub Trending 仓库列表",
  "inputSchema": {
    "type": "object",
    "properties": {
      "time_range": {
        "type": "string",
        "enum": ["daily", "weekly", "monthly"],
        "default": "daily"
      },
      "language": {
        "type": "string",
        "description": "编程语言筛选，例如: python, javascript, go"
      },
      "spoken_language": {
        "type": "string",
        "description": "自然语言筛选，例如: en, zh"
      }
    }
  }
}
```

## 4. 核心 MCP Tools 列表

### 4.1 GitHub 相关
- `get_github_trending_repos` - 获取 Trending 仓库
- `get_github_trending_developers` - 获取 Trending 开发者

### 4.2 Product Hunt 相关
- `get_producthunt_today` - 获取今日产品榜单
- `get_producthunt_week` - 获取本周产品榜单
- `get_producthunt_month` - 获取本月产品榜单
- `get_producthunt_upcoming` - 获取即将发布的产品

### 4.3 Hacker News 相关
- `get_hackernews_top` - 获取热门故事
- `get_hackernews_best` - 获取最佳故事
- `get_hackernews_ask` - 获取 Ask HN
- `get_hackernews_show` - 获取 Show HN

### 4.4 Reddit 相关
- `get_reddit_trending` - 获取指定 Subreddit 的热门帖子
- `get_reddit_sideproject` - 获取 r/SideProject 热门
- `get_reddit_indiebiz` - 获取创业相关 Subreddits 热门

### 4.5 Indie Hackers 相关
- `get_indiehackers_popular` - 获取热门帖子
- `get_indiehackers_income_reports` - 获取收入报告
- `get_indiehackers_milestones` - 获取项目里程碑

### 4.6 DevHunt 相关
- `get_devhunt_today` - 获取今日最佳开发工具
- `get_devhunt_week` - 获取本周最佳开发工具

### 4.7 AI & LLM 相关
- `get_openrouter_rankings` - 获取 OpenRouter LLM 排行
- `get_huggingface_trending_models` - 获取 Hugging Face 热门模型
- `get_huggingface_trending_spaces` - 获取 Hugging Face 热门 Spaces

### 4.8 收入排名相关
- `get_open_startup_rankings` - 获取公开创业公司收入排名
- `get_gumroad_top_creators` - 获取 Gumroad 畅销创作者

### 4.9 通用工具
- `search_trending_all` - 跨平台搜索热门内容
- `get_trending_summary` - 获取今日热门摘要（跨多个平台）

## 5. 数据格式规范

### 5.1 统一返回格式

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
      "title": "...",
      "url": "...",
      "description": "...",
      "stars": 1234,
      "language": "Python",
      "added_stars_today": 234,
      "contributors": [...]
    }
  ],
  "metadata": {
    "total_count": 25,
    "time_range": "daily",
    "language_filter": "python"
  }
}
```

## 6. 开发阶段规划

### Phase 1: 核心功能 (Week 1-2)
- [x] 项目初始化和架构搭建
- [ ] 实现 MCP Server 基础框架
- [ ] 实现 GitHub Trending (Repos & Developers)
- [ ] 实现 Product Hunt 榜单
- [ ] 实现 Hacker News 榜单
- [ ] 基础测试和文档

### Phase 2: 社区与讨论 (Week 3)
- [ ] 实现 Reddit 多个 Subreddit 榜单
- [ ] 实现 Indie Hackers 榜单
- [ ] 添加缓存机制
- [ ] 错误处理和日志系统

### Phase 3: AI 与收入类 (Week 4)
- [ ] 实现 OpenRouter LLM 排行
- [ ] 实现 Hugging Face Trending
- [ ] 实现 DevHunt 榜单
- [ ] 实现公开收入排名

### Phase 4: 优化与发布 (Week 5)
- [ ] 性能优化
- [ ] 完整的测试覆盖
- [ ] 完善文档和使用示例
- [ ] Docker 化部署
- [ ] 发布到 GitHub
- [ ] 在 Product Hunt 和 DevHunt 上发布

## 7. 配置与环境变量

```env
# API Keys
GITHUB_TOKEN=your_github_token
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
OPENROUTER_API_KEY=your_openrouter_key

# Cache Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_TTL=3600  # 1 hour

# Server Configuration
MCP_SERVER_PORT=3000
LOG_LEVEL=INFO

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=60
```

## 8. 非功能性需求

### 8.1 性能要求
- API 响应时间 < 2秒 (有缓存)
- API 响应时间 < 5秒 (无缓存)
- 支持并发查询

### 8.2 可靠性
- 单个榜单失败不影响其他榜单
- 自动重试机制
- 优雅降级

### 8.3 可维护性
- 模块化设计，易于添加新榜单
- 完善的日志和监控
- 清晰的代码注释和文档

### 8.4 安全性
- API Key 安全存储
- Rate Limiting 防止滥用
- 输入参数验证

## 9. 使用场景示例

### 场景 1: 开发者寻找灵感
```
User: 我想看看最近有什么热门的 Python 项目
AI: 调用 get_github_trending_repos(language="python", time_range="weekly")
返回: Top 25 Python trending repos
```

### 场景 2: 了解行业动态
```
User: 今天 Hacker News 和 Product Hunt 上有什么热门的？
AI: 并行调用 get_hackernews_top() 和 get_producthunt_today()
返回: 综合摘要
```

### 场景 3: 寻找成功案例
```
User: 有哪些独立开发者月收入超过 10k 的项目？
AI: 调用 get_indiehackers_income_reports() 和 get_open_startup_rankings()
返回: 高收入项目列表和分析
```

### 场景 4: 选择 LLM 模型
```
User: 我想找一个性价比高的 LLM API
AI: 调用 get_openrouter_rankings()
返回: 按性价比排序的模型列表
```

## 10. 竞品分析

### 现有方案
1. **手动访问各个网站** - 耗时且低效
2. **RSS 订阅** - 信息碎片化，无法聚合分析
3. **专门的聚合网站** - 覆盖不全，无 AI 集成

### 本产品优势
- MCP 协议原生支持 AI 助手集成
- 一站式聚合，覆盖独立开发者全生命周期
- 实时数据，支持自定义查询
- 开源免费，社区驱动

## 11. 市场推广计划

### 11.1 发布渠道
1. **Product Hunt** - 主要发布渠道
2. **DevHunt** - 开发者工具专属平台
3. **Hacker News Show HN** - 技术社区
4. **Reddit** - r/SideProject, r/webdev, r/programming
5. **Indie Hackers** - 分享构建过程
6. **Twitter/X** - #BuildInPublic 话题

### 11.2 内容营销
- 撰写技术博客: "如何构建一个 MCP Server"
- 制作使用教程视频
- 分享独立开发者数据洞察

## 12. 成功指标

### 12.1 用户指标
- GitHub Stars > 500 (第一个月)
- 活跃用户 > 1000 (第三个月)
- 社区贡献者 > 10

### 12.2 技术指标
- 榜单数据覆盖率 > 95%
- API 可用性 > 99%
- 平均响应时间 < 3秒

### 12.3 社区指标
- Product Hunt 排名 Top 5 (发布日)
- Hacker News 首页
- 10+ 篇博客/视频提及

## 13. 风险与挑战

### 13.1 技术风险
- **反爬虫机制**: 部分网站可能封禁爬虫 → 使用官方 API + 备用方案
- **API 限流**: GitHub 等有 API 调用限制 → 添加缓存和智能重试
- **数据结构变化**: 网站改版导致解析失败 → 版本锁定 + 自动告警

### 13.2 法律风险
- **版权问题**: 数据使用合规性 → 仅提供链接和摘要，不存储完整内容
- **服务条款**: 遵守各平台 TOS → 详细审查并遵守

### 13.3 运营风险
- **维护成本**: 长期维护压力 → 开源社区化，接受贡献
- **服务器成本**: 流量增长成本 → 鼓励用户自行部署

## 14. 后续扩展方向

### 14.1 功能扩展
- 支持自定义榜单订阅
- 添加榜单数据分析和可视化
- 提供 Webhook 通知功能
- AI 驱动的趋势预测

### 14.2 商业化可能
- Premium API (更高的调用频率)
- 企业版 (私有化部署)
- 数据报告订阅服务

## 15. 参考资料

### 15.1 官方文档
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [GitHub REST API](https://docs.github.com/en/rest)
- [Reddit API](https://www.reddit.com/dev/api/)
- [Hacker News API](https://github.com/HackerNews/API)

### 15.2 参考项目
- [mcp-github-trending](https://github.com/hetaoBackend/mcp-github-trending)
- [awesome-indiehackers](https://github.com/johackim/awesome-indiehackers)
- [indie-dev-toolkit](https://github.com/thedaviddias/indie-dev-toolkit)

---

**文档版本**: v1.0
**创建日期**: 2025-11-15
**最后更新**: 2025-11-15
**文档维护者**: Project Team
