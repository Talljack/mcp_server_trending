#!/bin/bash
# PyPI 部署脚本

set -e

echo "🚀 MCP Server Trending - PyPI 部署"
echo "=================================="
echo ""

# 1. 清理旧文件
echo "📦 步骤 1/4: 清理旧的构建文件..."
rm -rf dist/ build/ src/*.egg-info
echo "✅ 清理完成"
echo ""

# 2. 构建包
echo "🔨 步骤 2/4: 构建分发包..."
uv run python -m build
echo "✅ 构建完成"
echo ""

# 3. 验证包
echo "🔍 步骤 3/4: 验证包..."
uv run twine check dist/*
echo "✅ 验证完成"
echo ""

# 4. 上传选项
echo "📤 步骤 4/4: 上传到 PyPI"
echo ""
echo "请选择上传目标："
echo "  1) Test PyPI (测试环境，推荐先用这个)"
echo "  2) PyPI (正式环境)"
echo "  3) 取消"
echo ""
read -p "请输入选择 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "上传到 Test PyPI..."
        echo "提示: Username 输入 __token__"
        echo "      Password 输入你的 Test PyPI Token"
        echo ""
        uv run twine upload --repository testpypi dist/*
        echo ""
        echo "✅ 上传完成！"
        echo ""
        echo "测试安装命令:"
        echo "pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ mcp-server-trending"
        ;;
    2)
        echo ""
        echo "上传到正式 PyPI..."
        echo "提示: Username 输入 __token__"
        echo "      Password 输入你的 PyPI Token"
        echo ""
        uv run twine upload dist/*
        echo ""
        echo "✅ 上传完成！"
        echo ""
        echo "安装命令:"
        echo "pip install mcp-server-trending"
        ;;
    3)
        echo ""
        echo "❌ 已取消上传"
        echo ""
        echo "手动上传命令:"
        echo "  Test PyPI: uv run twine upload --repository testpypi dist/*"
        echo "  正式 PyPI: uv run twine upload dist/*"
        ;;
    *)
        echo ""
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "🎉 完成！"

