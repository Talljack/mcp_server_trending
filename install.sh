#!/bin/bash
# MCP Server Trending - 一键安装脚本

set -e  # 遇到错误立即退出

echo "🚀 MCP Server Trending - 一键安装"
echo "=================================="
echo ""

# 检测操作系统
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "📍 检测到系统: $MACHINE"
echo ""

# 获取项目路径
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

# 步骤 1: 检查 Python
echo "1️⃣  检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3"
    echo "请先安装 Python 3.10 或更高版本"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "   ✅ Python $PYTHON_VERSION"

# 步骤 2: 创建虚拟环境
echo ""
echo "2️⃣  创建虚拟环境..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "   ✅ 虚拟环境已创建"
else
    echo "   ℹ️  虚拟环境已存在"
fi

# 步骤 3: 安装依赖
echo ""
echo "3️⃣  安装依赖包..."
"$VENV_DIR/bin/pip" install -q --upgrade pip
"$VENV_DIR/bin/pip" install -q -e "$PROJECT_DIR"
echo "   ✅ 依赖安装完成"

# 步骤 4: 测试服务器
echo ""
echo "4️⃣  测试 MCP Server..."
if "$VENV_DIR/bin/python" "$PROJECT_DIR/tests/test_server_setup.py" > /dev/null 2>&1; then
    echo "   ✅ 服务器测试通过"
else
    echo "   ⚠️  服务器测试失败，但可能仍然可用"
fi

# 步骤 5: 生成配置
echo ""
echo "5️⃣  生成 MCP 配置..."

# Claude Desktop 配置
if [ "$MACHINE" = "Mac" ]; then
    CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    CONFIG_DIR=$(dirname "$CLAUDE_CONFIG")

    # 创建配置目录
    mkdir -p "$CONFIG_DIR"

    # 生成配置内容
    cat > /tmp/mcp_trending_config.json << EOF
{
  "trending": {
    "command": "$VENV_DIR/bin/mcp-server-trending"
  }
}
EOF

    echo "   📝 Claude Desktop 配置已生成"
    echo ""
    echo "   配置文件位置: /tmp/mcp_trending_config.json"
    echo ""

    # 如果配置文件存在，提示合并
    if [ -f "$CLAUDE_CONFIG" ]; then
        echo "   ⚠️  Claude Desktop 配置文件已存在"
        echo "   请手动将以下内容添加到 mcpServers 中:"
        echo ""
        cat /tmp/mcp_trending_config.json
        echo ""
    else
        # 创建新配置
        cat > "$CLAUDE_CONFIG" << EOF
{
  "mcpServers": {
    "trending": {
      "command": "$VENV_DIR/bin/mcp-server-trending"
    }
  }
}
EOF
        echo "   ✅ Claude Desktop 配置已自动添加"
    fi
fi

# Cherry Studio 配置
cat > /tmp/mcp_trending_cherry.json << EOF
{
  "name": "Trending",
  "description": "独立开发者热门榜单聚合服务",
  "type": "stdio",
  "command": "$VENV_DIR/bin/mcp-server-trending"
}
EOF

echo "   📝 Cherry Studio 配置已生成: /tmp/mcp_trending_cherry.json"

# 完成
echo ""
echo "=================================="
echo "✅ 安装完成！"
echo "=================================="
echo ""
echo "📚 下一步:"
echo ""

if [ "$MACHINE" = "Mac" ]; then
    echo "   Claude Desktop:"
    echo "   1. 重启 Claude Desktop"
    echo "   2. 开始使用！"
    echo ""
fi

echo "   Cherry Studio:"
echo "   1. 打开 Cherry Studio"
echo "   2. 设置 → MCP Server → 添加服务器"
echo "   3. 复制 /tmp/mcp_trending_cherry.json 中的配置"
echo "   4. 保存并重启"
echo ""
echo "🧪 测试查询:"
echo '   "请帮我查询 GitHub 上今天最热门的 Python 项目"'
echo ""
echo "📖 查看完整文档: $PROJECT_DIR/README.md"
echo ""
