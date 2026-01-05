#!/usr/bin/env python3
"""
辅助工具：获取飞书相关ID
帮助用户快速获取chat_id、user_id等信息
"""
import sys
import os
import json

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feishu_client import FeishuClient


def get_chat_list(client: FeishuClient):
    """获取群聊列表"""
    print("\n正在获取群聊列表...")
    try:
        result = client._request("GET", "/im/v1/chats", params={"page_size": 20})
        chats = result.get("data", {}).get("items", [])

        if not chats:
            print("未找到任何群聊")
            return

        print(f"\n找到 {len(chats)} 个群聊:")
        print("-" * 80)
        for i, chat in enumerate(chats, 1):
            chat_id = chat.get("chat_id", "")
            name = chat.get("name", "未命名群聊")
            description = chat.get("description", "")
            print(f"{i}. 群名: {name}")
            print(f"   群ID (chat_id): {chat_id}")
            if description:
                print(f"   描述: {description}")
            print()

    except Exception as e:
        print(f"获取群聊列表失败: {e}")


def get_user_list(client: FeishuClient):
    """获取部门用户列表"""
    print("\n正在获取用户列表...")
    try:
        result = client._request("GET", "/contact/v3/users", params={
            "page_size": 50,
            "department_id_type": "department_id"
        })
        users = result.get("data", {}).get("items", [])

        if not users:
            print("未找到任何用户")
            return

        print(f"\n找到 {len(users)} 个用户:")
        print("-" * 80)
        for i, user in enumerate(users, 1):
            user_id = user.get("user_id", "")
            name = user.get("name", "")
            en_name = user.get("en_name", "")
            email = user.get("email", "")

            print(f"{i}. 姓名: {name} ({en_name})")
            print(f"   用户ID (user_id): {user_id}")
            if email:
                print(f"   邮箱: {email}")
            print()

    except Exception as e:
        print(f"获取用户列表失败: {e}")


def search_chat_messages(client: FeishuClient, chat_id: str):
    """获取群聊最近的消息，帮助确认chat_id是否正确"""
    print(f"\n正在获取群聊 {chat_id} 的最近消息...")
    try:
        messages = client.get_chat_messages(chat_id=chat_id, page_size=10)

        if not messages:
            print("该群聊暂无消息")
            return

        print(f"\n找到 {len(messages)} 条最近消息:")
        print("-" * 80)
        for i, msg in enumerate(messages, 1):
            sender = msg.get("sender", {})
            sender_id = sender.get("id", "")
            content = client.parse_message_content(msg)
            msg_type = msg.get("msg_type", "")

            print(f"{i}. 发送者ID: {sender_id}")
            print(f"   消息类型: {msg_type}")
            print(f"   内容: {content[:100]}..." if len(content) > 100 else f"   内容: {content}")
            print()

    except Exception as e:
        print(f"获取消息失败: {e}")


def main():
    """主函数"""
    print("=" * 80)
    print("飞书ID获取工具")
    print("=" * 80)

    # 读取配置
    config_path = "config.json"
    if not os.path.exists(config_path):
        config_path = "config.example.json"
        if not os.path.exists(config_path):
            print("\n错误: 未找到配置文件")
            print("请先创建 config.json 并填写 app_id 和 app_secret")
            return

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return

    app_id = config.get('feishu', {}).get('app_id', '')
    app_secret = config.get('feishu', {}).get('app_secret', '')

    if not app_id or not app_secret or 'xxx' in app_id:
        print("\n错误: 请先在 config.json 中配置正确的 app_id 和 app_secret")
        return

    # 创建客户端
    client = FeishuClient(app_id=app_id, app_secret=app_secret)

    while True:
        print("\n" + "=" * 80)
        print("请选择操作:")
        print("1. 获取群聊列表（获取 chat_id）")
        print("2. 获取用户列表（获取 user_id）")
        print("3. 查看指定群聊的最近消息")
        print("0. 退出")
        print("=" * 80)

        choice = input("\n请输入选项 (0-3): ").strip()

        if choice == "1":
            get_chat_list(client)
        elif choice == "2":
            get_user_list(client)
        elif choice == "3":
            chat_id = input("请输入群聊ID (chat_id): ").strip()
            if chat_id:
                search_chat_messages(client, chat_id)
        elif choice == "0":
            print("\n再见!")
            break
        else:
            print("\n无效的选项，请重新选择")


if __name__ == '__main__':
    main()
