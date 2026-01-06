# 使用飞书 MCP 构建应用完全指南

本指南将一步步教你如何使用飞书官方 MCP 服务器来构建消息追踪应用。

## 什么是 MCP？

**MCP (Model Context Protocol)** 是 Anthropic 开发的标准协议，允许 AI 模型（如 Claude）通过统一接口与外部工具和服务通信。

### MCP vs 直接 API 调用

| 方式 | 优点 | 缺点 |
|------|------|------|
| **直接 API** | 完全控制，灵活 | 需要手动编写封装 |
| **MCP** | 标准化，AI 友好，自动发现 | 依赖 MCP 服务器 |

---

## 📦 步骤 1：安装飞书官方 MCP 服务器

### 1.1 检查环境

```bash
# 检查 Node.js（需要 LTS 版本）
node --version

# 检查 npm
npm --version
```

### 1.2 全局安装（可选）

```bash
npm install -g @larksuiteoapi/lark-mcp
```

或者使用 npx（推荐，无需全局安装）：
```bash
npx @larksuiteoapi/lark-mcp --help
```

---

## 🔧 步骤 2：配置 MCP 服务器

### 2.1 创建 Claude Code MCP 配置

Claude Code 需要在配置文件中声明 MCP 服务器。创建或编辑配置文件：

**位置**：
- macOS/Linux: `~/.config/claude-code/mcp_config.json`
- Windows: `%APPDATA%\claude-code\mcp_config.json`

**内容**：
```json
{
  "mcpServers": {
    "feishu": {
      "command": "npx",
      "args": [
        "-y",
        "@larksuiteoapi/lark-mcp",
        "mcp",
        "-a", "YOUR_APP_ID",
        "-s", "YOUR_APP_SECRET"
      ],
      "env": {
        "FEISHU_DOMAIN": "https://open.feishu.cn"
      }
    }
  }
}
```

### 2.2 配置说明

- **command**: 使用 `npx` 运行 MCP 服务器
- **args**:
  - `-y`: 自动确认安装
  - `@larksuiteoapi/lark-mcp`: 官方包名
  - `mcp`: MCP 模式
  - `-a`: App ID
  - `-s`: App Secret
- **env**:
  - `FEISHU_DOMAIN`: 飞书域名（国内版使用 `https://open.feishu.cn`，国际版使用 `https://open.larksuite.com`）

### 2.3 使用环境变量（更安全）

```json
{
  "mcpServers": {
    "feishu": {
      "command": "npx",
      "args": ["-y", "@larksuiteoapi/lark-mcp", "mcp", "-a", "${FEISHU_APP_ID}", "-s", "${FEISHU_APP_SECRET}"],
      "env": {
        "FEISHU_APP_ID": "cli_xxxxxxxx",
        "FEISHU_APP_SECRET": "xxxxxxxx",
        "FEISHU_DOMAIN": "https://open.feishu.cn"
      }
    }
  }
}
```

---

## 🎯 步骤 3：在 Claude Code 中使用 MCP

### 3.1 可用的 MCP 工具

飞书官方 MCP 提供的工具（部分）：

| 工具名 | 功能 | 用途 |
|--------|------|------|
| `mcp__feishu__get_messages` | 获取消息列表 | 追踪群聊消息 |
| `mcp__feishu__send_message` | 发送消息 | 发送通知 |
| `mcp__feishu__create_bitable_record` | 创建多维表格记录 | 保存数据 |
| `mcp__feishu__get_bitable_records` | 获取多维表格记录 | 读取数据 |
| `mcp__feishu__search_messages` | 搜索消息 | 查找特定内容 |

### 3.2 在代码中调用 MCP 工具

Claude Code 会自动识别可用的 MCP 工具。你可以直接在对话中请求：

```
"请使用 MCP 获取群聊 oc_xxx 的最近消息"
```

Claude 会自动调用对应的 MCP 工具。

---

## 💻 步骤 4：创建使用 MCP 的应用

### 4.1 项目结构

```
GTOlab-mcp/
├── mcp_config.json          # MCP 配置
├── config.json              # 应用配置
├── mcp_tracker.py           # 使用 MCP 的追踪器
└── docs/
    └── MCP_USAGE.md         # MCP 使用文档
```

### 4.2 应用配置（config.json）

```json
{
  "tracker": {
    "chat_id": "oc_xxxxxxxx",
    "target_user_id": "ou_xxxxxxxx",
    "bitable_app_token": "bascnxxxx",
    "bitable_table_id": "tblxxxx"
  },
  "schedule": {
    "run_time": "23:00",
    "timezone": "Asia/Shanghai"
  }
}
```

注意：App ID 和 App Secret 已在 MCP 配置中设置。

---

## 🔌 步骤 5：重启 Claude Code

配置 MCP 后，需要重启 Claude Code：

1. 关闭所有 Claude Code 窗口
2. 重新启动 Claude Code
3. MCP 服务器会自动连接

### 验证 MCP 连接

在 Claude Code 中询问：
```
"列出可用的飞书 MCP 工具"
```

如果配置成功，Claude 会列出所有可用的飞书 MCP 工具。

---

## 🎨 步骤 6：使用 MCP 重构应用

### 方式一：通过 Claude Code 自然语言

直接在 Claude Code 中说：

```
"使用飞书 MCP 工具获取群聊 oc_xxx 中用户 ou_xxx 的消息，
并将结果保存到多维表格 bascnxxx 的表 tblxxx 中"
```

Claude 会自动：
1. 调用 `mcp__feishu__get_messages` 获取消息
2. 筛选目标用户的消息
3. 调用 `mcp__feishu__create_bitable_record` 保存数据

### 方式二：编写 Python 脚本调用 MCP（高级）

虽然 MCP 主要用于 AI 交互，但也可以通过 MCP SDK 在 Python 中调用：

```python
# 需要安装 mcp 客户端库
# pip install mcp

from mcp import Client

async def use_mcp():
    async with Client("feishu") as client:
        # 获取消息
        messages = await client.call_tool(
            "mcp__feishu__get_messages",
            chat_id="oc_xxx",
            limit=100
        )

        # 保存到多维表格
        for msg in messages:
            await client.call_tool(
                "mcp__feishu__create_bitable_record",
                app_token="bascnxxx",
                table_id="tblxxx",
                fields=msg
            )
```

---

## 🔍 步骤 7：调试 MCP

### 查看 MCP 日志

MCP 服务器的日志通常在：
- macOS/Linux: `~/.config/claude-code/mcp_logs/`
- Windows: `%APPDATA%\claude-code\mcp_logs\`

### 常见问题

#### 1. MCP 服务器未启动

**症状**：Claude Code 提示找不到 MCP 工具

**解决**：
```bash
# 手动测试 MCP 服务器
npx @larksuiteoapi/lark-mcp mcp -a YOUR_APP_ID -s YOUR_APP_SECRET
```

#### 2. 权限不足

**症状**：MCP 调用返回权限错误

**解决**：检查飞书应用权限配置，确保已添加所需权限

#### 3. 网络问题

**症状**：MCP 请求超时

**解决**：检查网络连接和防火墙设置

---

## 📊 步骤 8：完整示例

### 示例：使用 MCP 追踪消息

在 Claude Code 中执行：

```
请帮我完成以下任务：
1. 使用 MCP 获取群聊 oc_abc123 的最近 24 小时消息
2. 筛选出用户 ou_def456 的消息
3. 将消息保存到多维表格 bascn789 的表 tbl012 中
4. 每条消息包含：日期、时间、用户名、消息内容、消息类型
```

Claude 会自动：
1. 调用 MCP 工具获取数据
2. 处理和筛选数据
3. 保存到多维表格
4. 返回执行结果

---

## ⚙️ 高级配置

### 使用多个 MCP 服务器

```json
{
  "mcpServers": {
    "feishu-prod": {
      "command": "npx",
      "args": ["-y", "@larksuiteoapi/lark-mcp", "mcp", "-a", "${PROD_APP_ID}", "-s", "${PROD_APP_SECRET}"]
    },
    "feishu-dev": {
      "command": "npx",
      "args": ["-y", "@larksuiteoapi/lark-mcp", "mcp", "-a", "${DEV_APP_ID}", "-s", "${DEV_APP_SECRET}"]
    }
  }
}
```

### 自定义 MCP 超时

```json
{
  "mcpServers": {
    "feishu": {
      "command": "npx",
      "args": ["..."],
      "timeout": 30000  // 30秒超时
    }
  }
}
```

---

## 🆚 MCP vs 直接 API 对比

### 我们之前的实现（直接 API）

```python
client = FeishuClient(app_id, app_secret)
messages = client.get_chat_messages(chat_id)
client.add_bitable_record(app_token, table_id, fields)
```

**优点**：完全控制，无依赖
**缺点**：需要手写封装，不能利用 AI 自动调用

### 使用 MCP

```
Claude，请获取群聊消息并保存到表格
```

**优点**：AI 友好，自动化，标准化
**缺点**：需要 MCP 服务器，功能受限于 MCP 实现

---

## 🚀 下一步

1. **安装并配置 MCP**：按照步骤 1-2 完成
2. **测试 MCP 连接**：按照步骤 5 验证
3. **使用 MCP 构建应用**：直接在 Claude Code 中用自然语言描述需求
4. **自动化**：设置定时任务调用 MCP 工具

---

## 📚 参考资源

- [飞书官方 MCP GitHub](https://github.com/larksuite/lark-openapi-mcp)
- [飞书开放平台 MCP 文档](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/mcp_integration/mcp_introduction)
- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Claude Code 文档](https://docs.anthropic.com/claude/docs)

---

## ❓ 常见问题

### Q: MCP 和直接 API 哪个更好？

**A**: 取决于使用场景：
- **原型和快速开发**：使用 MCP，让 AI 自动调用
- **生产环境**：使用直接 API，更稳定可控
- **最佳实践**：混合使用，MCP 用于交互，API 用于核心逻辑

### Q: 能否同时使用 MCP 和直接 API？

**A**: 可以！我们的应用可以保留原有的 API 封装，同时配置 MCP 供 Claude Code 使用。

### Q: MCP 支持哪些飞书功能？

**A**: 官方 MCP 支持：
- ✅ 消息管理
- ✅ 文档操作
- ✅ 多维表格
- ✅ 日历事件
- ❌ 文件上传下载（暂不支持）

---

准备好了吗？让我们开始配置 MCP 吧！
