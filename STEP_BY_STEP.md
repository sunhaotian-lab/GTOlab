# 手把手教你使用飞书 MCP - 超详细版

我会一步一步教你，每个步骤都非常详细。按照顺序做就可以了！

---

## 📋 开始前的检查清单

先确认以下信息，如果没有就跟着做：

### ✅ 检查 1：你有飞书应用吗？

**如果没有，按以下步骤创建：**

1. 打开浏览器，访问：https://open.feishu.cn/app
2. 使用你的飞书账号登录
3. 点击右上角的【创建企业自建应用】按钮
4. 填写信息：
   - **应用名称**：随便写，比如"消息追踪器"
   - **应用描述**：随便写，比如"自动追踪消息"
   - **应用图标**：可以不上传
5. 点击【确定】创建

**创建后，记下这两个重要信息：**
- **App ID**：格式像这样 `cli_a1b2c3d4e5f6g7h8`
- **App Secret**：格式像这样 `abcdefghijklmnopqrstuvwxyz123456`

**在哪里找？**
- 创建应用后，在【凭证与基础信息】页面可以看到
- 点击【查看】可以看到 App Secret

**⚠️ 重要**：把这两个值复制保存到记事本里，等会要用！

---

### ✅ 检查 2：配置应用权限

**步骤：**

1. 在飞书开放平台，打开你刚才创建的应用
2. 点击左侧菜单【权限管理】
3. 点击【添加权限】
4. 搜索并添加以下权限：
   - `im:message` - 获取与发送单聊、群组消息
   - `im:chat` - 获取群信息
   - `bitable:app` - 查看、评论和编辑多维表格
5. 点击【申请发布】
6. **如果你是管理员**：自己审批通过
7. **如果你不是管理员**：等待管理员审批

**怎么知道审批通过了？**
- 在【权限管理】页面，权限状态显示为【已开通】

---

### ✅ 检查 3：Node.js 环境

**检查是否已安装：**

打开终端（命令行），输入：

```bash
node --version
```

**如果看到版本号**（比如 v22.21.1），说明已安装，跳到下一步 ✅

**如果提示"command not found"或"未找到命令"**，需要安装：

**安装 Node.js：**
- **macOS**: 访问 https://nodejs.org/ 下载并安装
- **Linux**:
  ```bash
  # Ubuntu/Debian
  sudo apt update
  sudo apt install nodejs npm

  # CentOS
  sudo yum install nodejs npm
  ```
- **Windows**: 访问 https://nodejs.org/ 下载并安装

安装后，再次运行 `node --version` 确认成功。

---

## 🚀 正式开始：配置飞书 MCP

所有准备工作完成后，现在开始配置 MCP！

---

## 第 1 步：运行自动配置脚本

### 1.1 进入项目目录

打开终端，输入：

```bash
cd /home/user/GTOlab
```

**验证是否在正确目录：**
```bash
pwd
# 应该输出：/home/user/GTOlab
```

```bash
ls
# 应该能看到：setup_mcp.sh, README.md 等文件
```

---

### 1.2 运行配置脚本

```bash
./setup_mcp.sh
```

**如果提示"权限不足"**，运行：
```bash
chmod +x setup_mcp.sh
./setup_mcp.sh
```

---

### 1.3 按照提示输入信息

脚本会问你几个问题，按照下面回答：

**问题 1：App ID**
```
App ID:
```
**怎么答**：粘贴你之前保存的 App ID（比如 `cli_a1b2c3d4e5f6g7h8`）

**问题 2：App Secret**
```
App Secret:
```
**怎么答**：粘贴你之前保存的 App Secret

**问题 3：选择域名**
```
选择飞书域名：
1) 中国版 (https://open.feishu.cn)
2) 国际版 (https://open.larksuite.com)
请选择 (1/2):
```
**怎么答**：
- 如果你在中国使用飞书，输入 `1`
- 如果你使用国际版 Lark，输入 `2`

**问题 4：是否测试**
```
是否立即测试 MCP 服务器？(y/n):
```
**怎么答**：输入 `n`（先不测试，后面会一起测试）

---

### 1.4 看到成功提示

如果看到这样的输出，说明成功了：

```
==========================================
✅ MCP 配置已创建
==========================================

配置文件位置: /home/user/.config/claude-code/mcp_config.json

下一步：
1. 重启 Claude Code
2. 在 Claude Code 中输入：'列出可用的飞书 MCP 工具'
3. 如果看到工具列表，说明配置成功！
```

**🎉 恭喜！第 1 步完成！**

---

## 第 2 步：重启 Claude Code

### 2.1 完全关闭 Claude Code

**重要**：必须完全关闭，不是最小化！

- **macOS**:
  - 按 `Cmd + Q` 完全退出
  - 或者右键 Dock 图标，选择【退出】

- **Windows**:
  - 点击右上角 ❌ 关闭
  - 确保任务栏没有 Claude Code 图标

- **Linux**:
  - 完全关闭所有窗口
  - 运行 `pkill -9 claude` 确保进程结束

### 2.2 重新启动 Claude Code

正常打开 Claude Code 应用程序。

### 2.3 等待 MCP 连接

启动后等待 10-15 秒，让 MCP 服务器在后台启动。

**🎉 第 2 步完成！**

---

## 第 3 步：验证 MCP 是否配置成功

### 3.1 在 Claude Code 中输入测试命令

在 Claude Code 的对话框中，输入：

```
列出所有可用的飞书 MCP 工具
```

或者：

```
mcp tools list
```

### 3.2 检查返回结果

**✅ 成功的情况**：

你应该能看到类似这样的工具列表：

```
可用的飞书 MCP 工具：

1. mcp__feishu__get_messages - 获取群聊消息
2. mcp__feishu__send_message - 发送消息
3. mcp__feishu__create_bitable_record - 创建多维表格记录
4. mcp__feishu__get_bitable_records - 获取多维表格记录
... (还有更多工具)
```

**❌ 失败的情况**：

如果返回"没有找到 MCP 工具"或类似错误，跳到【故障排除】章节。

**🎉 如果看到工具列表，第 3 步完成！MCP 配置成功！**

---

## 第 4 步：获取必要的 ID

要使用 MCP，你需要知道：
1. **群聊 ID (chat_id)**：你要追踪的群
2. **用户 ID (user_id)**：你要追踪的人
3. **多维表格 ID (app_token 和 table_id)**：保存数据的地方

### 4.1 运行辅助工具

在终端中：

```bash
cd /home/user/GTOlab
python tools/get_ids.py
```

**如果提示"没有 config.json"**：
```bash
cp config.example.json config.json
nano config.json
```

编辑 config.json，填入你的 App ID 和 App Secret，然后保存（Ctrl+O，Enter，Ctrl+X）。

### 4.2 选择功能

工具会显示菜单：

```
请选择操作:
1. 获取群聊列表（获取 chat_id）
2. 获取用户列表（获取 user_id）
3. 查看指定群聊的最近消息
0. 退出
```

**获取群聊 ID**：
- 输入 `1`
- 找到你要追踪的群，复制它的 `chat_id`（比如 `oc_abc123...`）

**获取用户 ID**：
- 输入 `2`
- 找到你要追踪的用户，复制它的 `user_id`（比如 `ou_def456...`）

**保存这些 ID**：把它们记录到记事本里！

### 4.3 准备多维表格

**创建多维表格**：

1. 在飞书中，点击左侧【多维表格】
2. 点击【新建多维表格】
3. 创建一个新表格，命名为"消息追踪"
4. 在表格中创建以下字段（列）：
   - 日期（类型：日期）
   - 时间（类型：文本）
   - 用户名（类型：文本）
   - 消息内容（类型：文本）
   - 消息类型（类型：文本）
   - 消息ID（类型：文本）

**获取多维表格 ID**：

1. 打开你刚创建的多维表格
2. 查看浏览器地址栏，URL 格式如下：

```
https://xxx.feishu.cn/base/bascnXXXXXXXXXXXXXX?table=tblXXXXXXXXXXXX
```

3. 记录下：
   - **app_token**: `bascnXXXXXXXXXXXXXX`（base/ 后面的部分）
   - **table_id**: `tblXXXXXXXXXXXX`（table= 后面的部分）

**🎉 第 4 步完成！你现在有了所有需要的 ID！**

---

## 第 5 步：开始使用 MCP！

现在万事俱备，可以开始使用了！

### 5.1 第一个测试：获取群聊消息

在 Claude Code 中输入：

```
请使用飞书 MCP 获取群聊 [你的chat_id] 的最近 10 条消息
```

**记得替换**：把 `[你的chat_id]` 替换成真实的 chat_id！

**示例**：
```
请使用飞书 MCP 获取群聊 oc_abc123def456 的最近 10 条消息
```

**期望结果**：
Claude 会调用 MCP，然后显示消息列表。

---

### 5.2 完整的任务：追踪并保存消息

在 Claude Code 中输入：

```
请使用飞书 MCP 帮我完成以下任务：

1. 获取群聊 [你的chat_id] 最近 24 小时的消息
2. 筛选出用户 [你的user_id] 的消息
3. 将消息保存到多维表格：
   - app_token: [你的app_token]
   - table_id: [你的table_id]
4. 报告执行结果

请逐步执行，并告诉我每一步的结果。
```

**记得替换所有 [...] 中的内容**！

**完整示例**：
```
请使用飞书 MCP 帮我完成以下任务：

1. 获取群聊 oc_abc123def456 最近 24 小时的消息
2. 筛选出用户 ou_xyz789abc012 的消息
3. 将消息保存到多维表格：
   - app_token: bascn123456789
   - table_id: tbl987654321
4. 报告执行结果

请逐步执行，并告诉我每一步的结果。
```

**期望结果**：
- Claude 会自动调用多个 MCP 工具
- 获取消息、筛选、保存
- 返回详细的执行报告
- 你可以在多维表格中看到新增的数据！

**🎉 第 5 步完成！你已经成功使用 MCP 了！**

---

## 🎊 恭喜完成！

现在你已经掌握了如何使用飞书 MCP！

---

## 📝 日常使用

以后你只需要在 Claude Code 中用自然语言描述需求就可以了！

**示例 1：每日追踪**
```
请追踪群聊 oc_abc123 中用户 ou_xyz789 昨天的所有消息，保存到我的表格
```

**示例 2：搜索关键词**
```
在群聊 oc_abc123 中搜索包含"重要"的消息
```

**示例 3：统计分析**
```
分析用户 ou_xyz789 本周的消息统计
```

---

## 🔧 故障排除

### 问题 1：看不到 MCP 工具

**解决方法**：

1. 检查配置文件是否存在：
   ```bash
   cat ~/.config/claude-code/mcp_config.json
   ```

2. 检查 Node.js：
   ```bash
   node --version
   ```

3. 手动测试 MCP 服务器：
   ```bash
   npx @larksuiteoapi/lark-mcp mcp -a YOUR_APP_ID -s YOUR_APP_SECRET
   ```
   按 Ctrl+C 退出

4. 完全重启 Claude Code

---

### 问题 2：权限错误

**原因**：飞书应用权限不足

**解决**：
1. 访问 https://open.feishu.cn/app
2. 打开你的应用
3. 检查【权限管理】，确保权限已审批

---

### 问题 3：找不到群聊或用户

**解决**：
1. 确保应用已添加到群聊：
   - 打开飞书群聊
   - 点击群设置 > 群机器人
   - 添加你的应用

2. 使用工具验证 ID：
   ```bash
   python tools/get_ids.py
   ```

---

## 📚 更多资源

- **详细文档**：[docs/MCP_GUIDE.md](docs/MCP_GUIDE.md)
- **使用示例**：[docs/MCP_EXAMPLES.md](docs/MCP_EXAMPLES.md)
- **常见问题**：[docs/FAQ.md](docs/FAQ.md)

---

## 💬 需要帮助？

如果遇到问题：

1. 查看上面的【故障排除】
2. 阅读 [docs/FAQ.md](docs/FAQ.md)
3. 在 GitHub 提交 Issue
4. 直接在 Claude Code 中问我！

---

**祝你使用愉快！🎉**
