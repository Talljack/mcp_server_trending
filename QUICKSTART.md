# 快速开始指南

## 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. (可选) 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件
```

## 运行示例

### 方式一：运行示例脚本

```bash
python examples/basic_usage.py
```

这会展示所有三个平台的数据获取功能。

### 方式二：作为 MCP Server 运行

```bash
python src/mcp_server_trending/server.py
```

## 测试

运行单元测试：

```bash
# 安装测试依赖
pip install pytest pytest-asyncio

# 运行测试
pytest tests/ -v
```

## 集成到 Claude Desktop

1. 编辑 Claude Desktop 配置文件：
   - **MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. 添加配置：

```json
{
  "mcpServers": {
    "trending": {
      "command": "python",
      "args": [
        "/absolute/path/to/mcp_server_trending/src/mcp_server_trending/server.py"
      ]
    }
  }
}
```

3. 重启 Claude Desktop

## 使用示例

在 Claude Desktop 中，你可以这样询问：

- "Show me today's trending Python repositories on GitHub"
- "What are the top stories on Hacker News?"
- "Get this week's top products on Product Hunt"

## 开发

### 项目结构

```
mcp_server_trending/
├── src/mcp_server_trending/
│   ├── models/           # 数据模型
│   ├── fetchers/         # 数据获取
│   │   ├── github/
│   │   ├── hackernews/
│   │   └── producthunt/
│   ├── utils/            # 工具函数
│   ├── config.py         # 配置
│   └── server.py         # MCP Server
├── tests/                # 测试
├── examples/             # 示例代码
└── docs/                 # 文档
```

### 添加新平台

参考 [PRD.md](PRD.md) 中的开发计划。

## 故障排除

### 问题: 导入错误

确保从项目根目录运行，或将 `src/` 添加到 PYTHONPATH：

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### 问题: 网络请求失败

- 检查网络连接
- 某些平台可能有速率限制
- 尝试清除缓存

## 更多信息

- [完整文档](README.md)
- [产品需求文档](PRD.md)
- [贡献指南](CONTRIBUTING.md)
