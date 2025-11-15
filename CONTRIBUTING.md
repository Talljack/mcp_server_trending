# 贡献指南

感谢你考虑为 MCP Server Trending 做贡献！

## 如何贡献

### 报告 Bug

在 [GitHub Issues](https://github.com/yourusername/mcp_server_trending/issues) 创建 issue，包括：

- 问题描述
- 复现步骤
- 期望行为
- 实际行为
- 环境信息（Python 版本、操作系统等）

### 提出新功能

1. 先创建 issue 讨论功能需求
2. 等待维护者反馈
3. 获得批准后开始实现

### 提交代码

1. Fork 项目
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 编写代码和测试
4. 提交更改：`git commit -m 'Add some AmazingFeature'`
5. 推送到分支：`git push origin feature/AmazingFeature`
6. 创建 Pull Request

## 代码规范

### Python 风格

- 遵循 PEP 8
- 使用 Type Hints
- 最大行长度：100 字符
- 使用 Black 格式化代码
- 使用 Ruff 进行 linting

```bash
# 格式化代码
black src/ tests/

# 检查代码
ruff check src/ tests/

# 类型检查
mypy src/
```

### 文档字符串

使用 Google 风格的文档字符串：

```python
def fetch_data(param: str, limit: int = 10) -> Dict[str, Any]:
    """
    Fetch data from API.

    Args:
        param: Parameter description
        limit: Maximum number of items to fetch

    Returns:
        Dictionary containing fetched data

    Raises:
        ValueError: If param is invalid
    """
    pass
```

### 提交信息

- 使用清晰的提交信息
- 首行简短描述（50 字符内）
- 必要时添加详细说明

示例：
```
Add support for Reddit trending

- Implement Reddit fetcher
- Add data models
- Register MCP tools
- Update documentation
```

## 测试

### 编写测试

- 所有新功能必须包含测试
- 测试应该独立且可重复
- 使用清晰的测试名称

```python
def test_cache_expiry():
    """Test that cache entries expire correctly."""
    # Test implementation
    pass
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_cache.py

# 查看覆盖率
pytest --cov=src/mcp_server_trending tests/
```

## 添加新平台

遵循以下步骤添加新平台支持：

### 1. 创建数据模型

在 `src/mcp_server_trending/models/` 创建新文件：

```python
# models/newplatform.py
from dataclasses import dataclass
from .base import BaseModel

@dataclass
class NewPlatformItem(BaseModel):
    """Data model for NewPlatform items."""
    rank: int
    title: str
    url: str
    # ... 其他字段
```

### 2. 实现 Fetcher

在 `src/mcp_server_trending/fetchers/newplatform/` 创建：

```python
# fetchers/newplatform/fetcher.py
from ..base import BaseFetcher
from ...models.newplatform import NewPlatformItem

class NewPlatformFetcher(BaseFetcher):
    """Fetcher for NewPlatform data."""

    def get_platform_name(self) -> str:
        return "newplatform"

    async def fetch_items(self, **params) -> TrendingResponse:
        """Fetch items from NewPlatform."""
        # 实现
        pass
```

### 3. 注册 MCP Tool

在 `server.py` 中添加：

```python
# 在 list_tools() 中添加
Tool(
    name="get_newplatform_items",
    description="Get items from NewPlatform",
    inputSchema={...}
)

# 在 call_tool() 中处理
elif name == "get_newplatform_items":
    response = await self.newplatform_fetcher.fetch_items(...)
    return [TextContent(type="text", text=self._format_response(response))]
```

### 4. 添加测试

在 `tests/` 创建测试文件：

```python
# tests/test_newplatform.py
def test_newplatform_fetcher():
    """Test NewPlatform fetcher."""
    # 测试实现
    pass
```

### 5. 更新文档

- 更新 README.md
- 更新 PRD.md
- 添加使用示例

## 项目结构规范

- **模块化**：每个平台独立文件夹
- **复用性**：使用 BaseFetcher 和 BaseModel
- **类型安全**：使用完整的类型标注
- **文档完善**：所有公共 API 需要文档字符串

## Code Review

Pull Request 会由维护者 review：

- 代码质量
- 测试覆盖率
- 文档完整性
- 性能影响

## 许可证

提交代码即表示你同意以 MIT 许可证发布你的贡献。

## 问题？

如有疑问，请在 issue 中提问或联系维护者。

谢谢你的贡献！🎉
