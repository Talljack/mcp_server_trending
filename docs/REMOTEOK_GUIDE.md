# RemoteOK 使用指南

## ✅ API 完全可用（2025年11月实测）

RemoteOK 提供**官方公开 JSON API**，无需注册、无需 API Key，完全免费！

### 📊 API 基本信息

```bash
URL: https://remoteok.com/api
方法: GET
认证: 不需要
频率限制: 无明确限制（建议合理使用）
数据更新: 实时更新
```

### 🎯 API 返回格式

```json
[
  // [0] 第一条是表头/元数据（需跳过）
  {
    "legal": "...",
    "description": "..."
  },

  // [1] 第二条开始才是真实职位
  {
    "id": "123456",
    "position": "Senior Python Developer",
    "company": "Acme Corp",
    "company_logo": "https://...",
    "tags": ["python", "remote", "backend", "api"],
    "salary": "$80k-$120k",
    "location": "🌍 Worldwide",
    "date": "2025-11-17",
    "url": "https://remoteok.com/remote-jobs/123456",
    "description": "We are looking for...",
    "apply_url": "https://..."
  },

  // 更多职位...
]
```

### 🚀 快速开始

#### 方法 1：使用 MCP Server Trending（推荐）

```python
# 通过 AI 助手查询
"帮我找 10 个 Python 相关的远程工作"
"查看最新的全栈开发远程职位"
"筛选薪资 >$100k 的远程工作"
```

#### 方法 2：直接使用 API

```bash
# 获取所有职位
curl https://remoteok.com/api | jq '.[1:10]'

# 只看 Python 职位
curl https://remoteok.com/api | jq '.[] | select(.tags[]? == "python")'

# 保存为 CSV
curl -s https://remoteok.com/api | \
  python3 -c "
import sys, json, csv
data = json.load(sys.stdin)[1:]  # 跳过第一条表头
writer = csv.writer(sys.stdout)
writer.writerow(['Company', 'Position', 'Salary', 'Tags', 'URL'])
for job in data[:50]:
    writer.writerows([[
        job.get('company', ''),
        job.get('position', ''),
        job.get('salary', ''),
        '|'.join(job.get('tags', [])),
        job.get('url', '')
    ]])
" > remoteok_jobs.csv
```

#### 方法 3：使用 Python 脚本

```python
import requests

# 获取职位数据
response = requests.get("https://remoteok.com/api", headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

jobs = response.json()[1:]  # 跳过第一条表头

# 筛选 Python 职位
python_jobs = [
    job for job in jobs
    if any('python' in tag.lower() for tag in job.get('tags', []))
]

print(f"找到 {len(python_jobs)} 个 Python 职位")

for job in python_jobs[:5]:
    print(f"\n职位: {job.get('position')}")
    print(f"公司: {job.get('company')}")
    print(f"薪资: {job.get('salary', 'N/A')}")
    print(f"标签: {', '.join(job.get('tags', [])[:5])}")
    print(f"链接: {job.get('url')}")
```

### ⚠️ 网络环境要求

RemoteOK API 会阻止部分网络环境：

**被阻止的情况：**
- ❌ 使用 VPN（大部分商业 VPN）
- ❌ 使用代理服务器
- ❌ 数据中心 IP
- ❌ 云服务器直接访问（AWS、GCP、Azure 等）

**允许访问的情况：**
- ✅ 家庭宽带网络
- ✅ 手机移动网络
- ✅ 办公网络（非数据中心）
- ✅ 咖啡馆/公共 WiFi

**错误提示：**
```
Disable your VPN to access Remote OK
```

### 🛠️ 故障排除

#### 问题 1：收到 "Disable your VPN" 错误

**解决方案：**
```bash
# 1. 关闭 VPN/代理
# 2. 使用手机热点测试
# 3. 或等待我们的智能降级功能（会自动切换到网页抓取）
```

#### 问题 2：返回空数据

**检查：**
```python
import requests
response = requests.get("https://remoteok.com/api")

# 检查状态码
print(f"状态码: {response.status_code}")

# 检查响应类型
print(f"Content-Type: {response.headers.get('content-type')}")

# 查看原始响应
print(f"响应内容: {response.text[:100]}")
```

#### 问题 3：在云服务器上无法访问

**解决方案：**
- 使用我们的智能降级功能（代码已实现）
- 或通过本地机器中转请求

### 📚 高级用法

#### 按薪资筛选

```python
# 只看高薪职位（>$100k）
high_salary_jobs = [
    job for job in jobs
    if job.get('salary') and any(
        str(n) in job['salary']
        for n in range(100, 300)
    )
]
```

#### 按地区筛选

```python
# 只看欧洲/英国职位
eu_jobs = [
    job for job in jobs
    if any(region in job.get('location', '').lower()
           for region in ['uk', 'europe', 'london', 'berlin'])
]
```

#### 按技能标签筛选

```python
# 全栈工程师（需要前后端技能）
fullstack_jobs = [
    job for job in jobs
    if (any(tag in job.get('tags', []) for tag in ['react', 'vue', 'angular']) and
        any(tag in job.get('tags', []) for tag in ['python', 'nodejs', 'java']))
]
```

### 🎉 总结

**RemoteOK API 优点：**
- ✅ 完全免费，无需注册
- ✅ 数据实时更新
- ✅ JSON 格式，易于解析
- ✅ 包含完整职位信息（公司、薪资、标签、链接）
- ✅ 无频率限制（合理使用）

**注意事项：**
- ⚠️ 需要非 VPN 网络环境
- ⚠️ 第一条数据是表头，需跳过
- ⚠️ 薪资信息可能为空（部分职位不公开）

**MCP Server Trending 已完整实现：**
- ✅ 自动跳过表头
- ✅ 智能标签过滤
- ✅ 关键词搜索
- ✅ API 失败时自动降级到网页抓取
- ✅ 清晰的错误提示

开始使用吧！🚀
