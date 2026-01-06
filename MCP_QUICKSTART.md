# MCP 快速开始（5分钟上手）

这是最简单的 MCP 配置指南，5分钟内让你开始使用飞书 MCP。

## 第 1 步：运行配置脚本（1分钟）

```bash
cd GTOlab
./setup_mcp.sh
```

按照提示输入：
1. 你的飞书 App ID
2. 你的飞书 App Secret
3. 选择域名（中国版/国际版）

脚本会自动创建 MCP 配置文件。

## 第 2 步：重启 Claude Code（30秒）

1. 完全关闭 Claude Code
2. 重新启动 Claude Code

## 第 3 步：测试 MCP（1分钟）

在 Claude Code 中输入：

```
列出可用的飞书 MCP 工具
```

如果看到工具列表，说明配置成功！✅

## 第 4 步：开始使用（2分钟）

在 Claude Code 中输入你的需求，例如：

```
请使用飞书 MCP 获取群聊 oc_xxx 的最近消息，
筛选出用户 ou_xxx 的发言，
并保存到多维表格 bascnxxx 的表 tblxxx
```

Claude 会自动调用 MCP 完成任务！

## 搞定！🎉

现在你可以：
- 用自然语言描述需求
- Claude 自动调用飞书 API
- 无需编写任何代码

## 进阶学习

- [完整 MCP 指南](docs/MCP_GUIDE.md) - 深入了解 MCP 配置
- [MCP 使用示例](docs/MCP_EXAMPLES.md) - 更多实际案例

## 遇到问题？

1. 检查 Node.js 是否安装：`node --version`
2. 查看配置文件：`~/.config/claude-code/mcp_config.json`
3. 查看 [FAQ](docs/FAQ.md) 或提交 Issue

---

**提示**：如果不想用脚本，也可以手动配置，参考 `mcp_config.example.json`。
