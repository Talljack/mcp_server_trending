# Reddit 智能主题查询功能 🎯

## ✨ 新功能简介

基于您的建议，我添加了 **Reddit 智能主题查询**功能！现在用户可以：

1. **精确查询** - 指定具体的 subreddit（保留原功能）
2. **智能查询** - 说出主题关键词，系统自动匹配相关 subreddits

---

## 🆕 新增的 MCP Tool

### `get_reddit_by_topic`

**功能**: 根据主题关键词自动选择相关 subreddits 并聚合热门内容

**参数**:
```json
{
  "topic": "ai",           // 可选，不提供则默认返回 indie 内容
  "sort_by": "hot",       // hot | top
  "time_range": "day",    // hour | day | week | month | year | all
  "limit": 50,            // 最多返回帖子数
  "use_cache": true
}
```

---

## 🎯 支持的主题

### AI & 机器学习
- **ai** → r/MachineLearning, r/artificial, r/ChatGPT, r/OpenAI, r/StableDiffusion, r/LocalLLaMA
- **ml** → r/MachineLearning, r/learnmachinelearning, r/datascience, r/deeplearning

### 加密货币 & 区块链
- **crypto** → r/cryptocurrency, r/Bitcoin, r/ethereum, r/CryptoMarkets
- **blockchain** → r/blockchain, r/ethereum, r/Bitcoin

### 创业 & 独立开发
- **indie** → r/SideProject, r/Entrepreneur, r/EntrepreneurRideAlong, r/startups *(默认)*
- **startup** → r/startups, r/Entrepreneur, r/smallbusiness, r/SideProject
- **saas** → r/SaaS, r/microSaaS, r/startups

### 编程语言
- **programming** → r/programming, r/learnprogramming, r/webdev, r/coding
- **python** → r/Python, r/learnpython, r/django, r/flask
- **javascript** → r/javascript, r/node, r/reactjs, r/vuejs

### Web & 移动开发
- **web** → r/webdev, r/web_design, r/Frontend, r/Backend
- **mobile** → r/androiddev, r/iOSProgramming, r/reactnative, r/FlutterDev

### 设计 & UI/UX
- **design** → r/web_design, r/UI_Design, r/UXDesign, r/graphic_design

### 商业 & 营销
- **business** → r/Entrepreneur, r/smallbusiness, r/business, r/marketing
- **marketing** → r/marketing, r/digital_marketing, r/SEO

### 自由职业 & 远程工作
- **freelance** → r/freelance, r/forhire, r/digitalnomad
- **remote** → r/digitalnomad, r/RemoteJobs, r/WorkOnline

### 其他领域
- **gaming** → r/gaming, r/gamedev, r/IndieGaming, r/Unity3D
- **iot** → r/IOT, r/homeautomation, r/raspberry_pi
- **devops** → r/devops, r/kubernetes, r/docker, r/aws
- **security** → r/netsec, r/cybersecurity, r/hacking

**总计 20+ 个主题类别，覆盖 100+ 个 subreddits**

---

## 💬 使用示例

### 示例 1: AI 相关内容
**用户**: "Reddit 上最近有什么 AI 的热门讨论？"

**Claude 调用**:
```python
get_reddit_by_topic(topic="ai", sort_by="hot", time_range="day")
```

**系统行为**:
1. 识别主题 "ai"
2. 自动查询: r/MachineLearning, r/artificial, r/ChatGPT, r/OpenAI, r/StableDiffusion, r/LocalLLaMA
3. 聚合并按分数排序
4. 返回前 50 条热门帖子

---

### 示例 2: 加密货币
**用户**: "最近 crypto 有什么新闻？"

**Claude 调用**:
```python
get_reddit_by_topic(topic="crypto", time_range="week")
```

**查询 subreddits**: r/cryptocurrency, r/Bitcoin, r/ethereum, r/CryptoMarkets

---

### 示例 3: 独立开发者内容（默认）
**用户**: "Reddit 上独立开发者在讨论什么？"

**Claude 调用**:
```python
get_reddit_by_topic()  # 不提供 topic，使用默认
```

**查询 subreddits**: r/SideProject, r/Entrepreneur, r/EntrepreneurRideAlong, r/startups

---

### 示例 4: Python 相关
**用户**: "Python 社区最近有什么热门项目？"

**Claude 调用**:
```python
get_reddit_by_topic(topic="python", sort_by="top", time_range="week")
```

**查询 subreddits**: r/Python, r/learnpython, r/django, r/flask

---

## 🔄 两种查询方式对比

### 1. 精确查询（原有功能）
```python
# 适用场景：明确知道要查哪个 subreddit
get_reddit_trending(subreddit="sideproject", sort_by="hot")
```

**优点**:
- 精确控制
- 单一来源

---

### 2. 智能查询（新功能）✨
```python
# 适用场景：想看某个主题的综合讨论
get_reddit_by_topic(topic="ai")
```

**优点**:
- 自动匹配多个相关 subreddits
- 聚合多源内容
- 按热度排序
- 更全面的视角

---

## 🚀 技术实现

### 主题映射
```python
TOPIC_SUBREDDITS = {
    "ai": ["MachineLearning", "ChatGPT", "OpenAI", ...],
    "crypto": ["cryptocurrency", "Bitcoin", "ethereum", ...],
    "indie": ["SideProject", "Entrepreneur", ...],
    ...
}
```

### 智能匹配逻辑
1. **精确匹配**: 如果输入 "ai"，直接匹配预定义的 AI subreddits
2. **模糊匹配**: 如果输入 "machine learning"，匹配包含相关词的主题
3. **后备方案**: 如果没有匹配，将输入当作 subreddit 名称

### 查询优化
- 限制最多查询 10 个 subreddits（避免请求过多）
- 每个 subreddit 限制 10 条帖子
- 聚合后按分数排序
- 返回前 N 条（默认 50）

---

## 📊 完整功能对比

| 功能 | get_reddit_trending | get_reddit_by_topic |
|------|---------------------|---------------------|
| **使用场景** | 精确查询单个 subreddit | 按主题聚合多个 subreddits |
| **Subreddit 选择** | 手动指定（必需） | 自动匹配（可选） |
| **查询数量** | 1 个 subreddit | 最多 10 个 subreddits |
| **排序** | 来源的原始排序 | 跨源按分数排序 |
| **默认行为** | 必须指定 subreddit | 不指定则返回 indie 内容 |
| **适合人群** | 熟悉 Reddit 的用户 | 所有用户 |

---

## 🎯 推荐使用场景

### 使用 `get_reddit_by_topic` 当:
- ✅ 想要某个领域的综合讨论（如 "AI"）
- ✅ 不确定应该查哪个具体 subreddit
- ✅ 想要多个相关社区的热门内容
- ✅ 快速了解某个主题的热点

### 使用 `get_reddit_trending` 当:
- ✅ 明确知道要查的 subreddit
- ✅ 只关心特定社区的内容
- ✅ 需要该社区的完整排名

---

## 🎉 总结

这个功能让 Reddit 查询变得更加**智能**和**用户友好**：

1. **用户不需要知道具体的 subreddit 名称**
2. **一次查询即可获取多个相关社区的内容**
3. **自动聚合和排序，给出最热门的讨论**
4. **支持 20+ 个主题，覆盖技术、创业、设计等各个领域**

**这正是您想要的效果！** 🎊

用户说 "我想看 AI 排行"，系统会自动找到所有 AI 相关的 subreddits，然后返回最热门的讨论。
