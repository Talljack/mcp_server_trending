# 🔧 Ruff 配置说明

## ✅ 已完成的配置

### 1. Ruff 规则配置 (`pyproject.toml`)

```toml
[tool.ruff]
line-length = 100
target-version = "py310"
fix = true  # 启用自动修复

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes (包括 F401 未使用的导入)
    "I",   # isort (自动排序导入)
    "UP",  # pyupgrade
]
fixable = ["ALL"]  # 所有规则都可以自动修复
ignore = [
    "E501",  # 行太长 - 描述字符串可以超过 100 字符
]
```

**启用的规则**：
- ✅ **F401**: 自动移除未使用的导入（如 `Dict`, `Optional`）
- ✅ **I**: 自动排序和组织导入语句
- ✅ **E/W**: 代码风格检查
- ✅ **UP**: Python 语法升级建议

**忽略的规则**：
- ⚠️ **E501**: 行太长（允许描述字符串超过 100 字符）

### 2. VS Code 配置 (`.vscode/settings.json`)

```json
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    },
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "ruff.enable": true,
  "ruff.lint.enable": true,
  "ruff.fixAll": true,
  "ruff.organizeImports": true
}
```

**功能**：
- ✅ 保存时自动格式化代码
- ✅ 保存时自动修复所有可修复的问题
- ✅ 保存时自动组织导入语句
- ✅ 自动移除未使用的导入

---

## 🚀 使用方法

### 方式一：VS Code 自动修复（推荐）

1. **安装 Ruff 扩展**
   - 打开 VS Code
   - 安装 "Ruff" 扩展（charliermarsh.ruff）

2. **保存文件时自动修复**
   - 编辑 Python 文件
   - `Cmd+S` (Mac) / `Ctrl+S` (Windows) 保存
   - 自动移除未使用的导入 ✨

### 方式二：命令行手动修复

```bash
# 检查所有问题
uv run ruff check src/

# 自动修复所有可修复的问题
uv run ruff check --fix src/

# 只检查特定文件
uv run ruff check src/mcp_server_trending/server.py

# 格式化代码
uv run ruff format src/
```

---

## 📝 常见问题

### Q1: 为什么保存时没有自动移除未使用的导入？

**可能的原因**：

1. **没有安装 Ruff 扩展**
   ```bash
   # 在 VS Code 中搜索并安装 "Ruff" 扩展
   ```

2. **配置文件没有生效**
   - 重新加载 VS Code 窗口: `Cmd+Shift+P` → "Reload Window"
   - 检查 `.vscode/settings.json` 是否存在

3. **Ruff 扩展被禁用**
   - 检查 VS Code 设置: `"ruff.enable": true`

### Q2: 如何只检查未使用的导入？

```bash
# 只检查 F401 规则（未使用的导入）
uv run ruff check --select F401 src/
```

### Q3: 如何临时禁用某个规则？

在代码中添加注释：

```python
from typing import Dict, Optional  # noqa: F401  # 临时禁用这一行的 F401 检查
```

或者在文件开头：

```python
# ruff: noqa: F401
```

### Q4: 如何查看所有可用的规则？

```bash
uv run ruff rule --all
```

---

## 🎯 实际效果

### 修复前

```python
from typing import Any, Dict, Optional  # Dict 和 Optional 未使用

def foo(x: Any):
    return x
```

### 修复后（保存时自动）

```python
from typing import Any  # 自动移除未使用的导入

def foo(x: Any):
    return x
```

---

## 🔍 检查整个项目

```bash
# 检查所有 Python 文件
uv run ruff check src/ tests/

# 自动修复所有问题
uv run ruff check --fix src/ tests/

# 查看详细报告
uv run ruff check --output-format=github src/
```

---

## 📚 更多信息

- **Ruff 官方文档**: https://docs.astral.sh/ruff/
- **VS Code 扩展**: https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff
- **规则列表**: https://docs.astral.sh/ruff/rules/

---

## ✨ 总结

现在你的项目已经配置好了自动代码检查和修复：

1. ✅ 保存文件时自动移除未使用的导入
2. ✅ 自动排序和组织导入语句
3. ✅ 自动修复代码风格问题
4. ✅ 保持代码整洁和一致

**只需要 `Cmd+S` 保存，一切自动完成！** 🎉

