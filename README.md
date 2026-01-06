# 飞书消息追踪器

自动追踪飞书群聊中特定用户的消息，并记录到飞书多维表格中。

## 功能特性

- 定时抓取飞书群聊消息
- 筛选特定用户的发言
- 自动记录到飞书多维表格
- 支持每日定时执行
- **🆕 支持 MCP (Model Context Protocol) 集成**

## 使用方式

本项目提供两种使用方式：

### 方式一：传统 Python 脚本（已实现）
直接运行 Python 脚本，适合：
- 需要完全控制的场景
- 服务器部署
- 定时任务自动化

### 方式二：MCP 集成（推荐用于 AI 交互）
通过 MCP 协议让 Claude Code 直接调用飞书 API，适合：
- AI 辅助开发
- 交互式操作
- 快速原型开发

**详细指南**：
- [MCP 完整使用指南](docs/MCP_GUIDE.md) - 一步步配置 MCP
- [MCP 使用示例](docs/MCP_EXAMPLES.md) - 实际使用案例

## 使用前准备

### 1. 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 点击"创建企业自建应用"
3. 填写应用名称和描述
4. 创建完成后，获取 `App ID` 和 `App Secret`

### 2. 配置应用权限

在"权限管理"中添加以下权限：

**消息相关权限：**
- `im:message:read` - 读取群聊消息
- `im:chat:read` - 获取群组信息

**多维表格权限：**
- `bitable:app:read` - 读取多维表格
- `bitable:app:write` - 写入多维表格

### 3. 获取必要的 ID

**群聊 ID (chat_id):**
1. 在飞书群聊中，点击群设置
2. 在群设置的 URL 中可以找到 chat_id

**用户 ID (user_id):**
- 方式1: 在飞书管理后台查看用户信息
- 方式2: 通过应用调用用户接口获取

**多维表格信息:**
- `app_token`: 多维表格的 URL 中包含
- `table_id`: 打开具体数据表，URL 中可以找到

## 安装

```bash
# 克隆仓库
git clone <repository-url>
cd GTOlab

# 安装依赖
pip install -r requirements.txt
```

## 配置

复制 `config.example.json` 为 `config.json` 并填写配置：

```json
{
  "feishu": {
    "app_id": "你的应用ID",
    "app_secret": "你的应用密钥"
  },
  "tracker": {
    "chat_id": "群聊ID",
    "target_user_id": "要追踪的用户ID",
    "bitable_app_token": "多维表格token",
    "bitable_table_id": "数据表ID"
  },
  "schedule": {
    "run_time": "23:00",
    "timezone": "Asia/Shanghai"
  }
}
```

## 使用方法

### 运行一次（手动测试）

```bash
python main.py --once
```

### 启动定时任务

```bash
python main.py
```

程序将按照配置的时间（默认每天23:00）自动执行。

## 多维表格字段说明

应用会在多维表格中创建/写入以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 日期 | 日期 | 消息发送日期 |
| 时间 | 文本 | 消息发送时间 |
| 用户名 | 文本 | 发言用户名称 |
| 消息内容 | 文本 | 消息内容 |
| 消息类型 | 文本 | 消息类型（文本/图片/文件等） |
| 消息ID | 文本 | 消息唯一标识 |

## 注意事项

1. 确保飞书应用已添加到目标群聊中
2. 应用需要获得管理员审批权限才能访问消息
3. 建议使用服务器或云函数持续运行
4. 注意保护 `config.json` 文件，不要泄露密钥

## 常见问题

**Q: 提示"权限不足"怎么办？**
A: 检查应用权限配置，确保已添加所需权限并通过审批。

**Q: 获取不到消息？**
A: 确保应用已被添加到目标群聊中。

**Q: 如何获取历史消息？**
A: 修改 `main.py` 中的时间范围参数即可。

## 技术栈

### Python 脚本方式
- Python 3.8+
- 飞书开放平台 API
- APScheduler (定时任务)

### MCP 方式
- Node.js (LTS)
- 飞书官方 MCP 服务器 (@larksuiteoapi/lark-mcp)
- Claude Code 或其他 MCP 兼容客户端

## 文档导航

- [README.md](README.md) - 项目概览（当前文档）
- [快速开始指南](docs/QUICKSTART.md) - 10分钟快速上手
- [部署指南](docs/DEPLOYMENT.md) - 详细部署方案
- [常见问题解答](docs/FAQ.md) - 38+ 常见问题
- **[MCP 使用指南](docs/MCP_GUIDE.md)** - MCP 完整配置步骤 ⭐
- **[MCP 示例](docs/MCP_EXAMPLES.md)** - MCP 实际使用案例 ⭐

## 许可证

MIT License
