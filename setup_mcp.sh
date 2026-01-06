#!/bin/bash
# 飞书 MCP 快速配置脚本

echo "=========================================="
echo "  飞书 MCP 服务器配置向导"
echo "=========================================="
echo

# 检查 Node.js
echo "检查 Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ 未安装 Node.js"
    echo "请访问 https://nodejs.org/ 下载安装"
    exit 1
fi
echo "✅ Node.js 版本: $(node --version)"
echo

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo "❌ 未安装 npm"
    exit 1
fi
echo "✅ npm 版本: $(npm --version)"
echo

# 测试 MCP 包
echo "测试飞书 MCP 包..."
if npx -y @larksuiteoapi/lark-mcp --help &> /dev/null; then
    echo "✅ 飞书 MCP 包可用"
else
    echo "❌ 无法访问飞书 MCP 包"
    echo "请检查网络连接"
    exit 1
fi
echo

# 提示输入配置
echo "请输入飞书应用信息："
echo

read -p "App ID: " APP_ID
read -p "App Secret: " APP_SECRET

# 选择域名
echo
echo "选择飞书域名："
echo "1) 中国版 (https://open.feishu.cn)"
echo "2) 国际版 (https://open.larksuite.com)"
read -p "请选择 (1/2): " DOMAIN_CHOICE

if [ "$DOMAIN_CHOICE" = "2" ]; then
    DOMAIN="https://open.larksuite.com"
else
    DOMAIN="https://open.feishu.cn"
fi

# 确定配置文件位置
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    CONFIG_DIR="$HOME/.config/claude-code"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    CONFIG_DIR="$HOME/.config/claude-code"
else
    # Windows (Git Bash)
    CONFIG_DIR="$APPDATA/claude-code"
fi

CONFIG_FILE="$CONFIG_DIR/mcp_config.json"

# 创建配置目录
mkdir -p "$CONFIG_DIR"

# 生成配置文件
cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "feishu": {
      "command": "npx",
      "args": [
        "-y",
        "@larksuiteoapi/lark-mcp",
        "mcp",
        "-a",
        "$APP_ID",
        "-s",
        "$APP_SECRET"
      ],
      "env": {
        "FEISHU_DOMAIN": "$DOMAIN"
      }
    }
  }
}
EOF

echo
echo "=========================================="
echo "✅ MCP 配置已创建"
echo "=========================================="
echo
echo "配置文件位置: $CONFIG_FILE"
echo
echo "下一步："
echo "1. 重启 Claude Code"
echo "2. 在 Claude Code 中输入：'列出可用的飞书 MCP 工具'"
echo "3. 如果看到工具列表，说明配置成功！"
echo
echo "测试命令："
echo "  npx @larksuiteoapi/lark-mcp mcp -a $APP_ID -s $APP_SECRET"
echo

# 询问是否测试
read -p "是否立即测试 MCP 服务器？(y/n): " TEST_CHOICE
if [ "$TEST_CHOICE" = "y" ] || [ "$TEST_CHOICE" = "Y" ]; then
    echo
    echo "启动 MCP 服务器测试（按 Ctrl+C 退出）..."
    npx @larksuiteoapi/lark-mcp mcp -a "$APP_ID" -s "$APP_SECRET"
fi
