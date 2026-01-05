"""
飞书API客户端封装
"""
import requests
import time
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class FeishuClient:
    """飞书开放平台API客户端"""

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.tenant_access_token = None
        self.token_expire_time = 0
        self.base_url = "https://open.feishu.cn/open-apis"

    def _get_tenant_access_token(self) -> str:
        """获取tenant_access_token"""
        if self.tenant_access_token and time.time() < self.token_expire_time:
            return self.tenant_access_token

        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"获取token失败: {result.get('msg')}")

        self.tenant_access_token = result["tenant_access_token"]
        self.token_expire_time = time.time() + result["expire"] - 300

        return self.tenant_access_token

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """统一请求方法"""
        token = self._get_tenant_access_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        headers["Content-Type"] = "application/json; charset=utf-8"

        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=headers, **kwargs)
        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"API请求失败: {result.get('msg')}")

        return result

    def get_chat_messages(
        self,
        chat_id: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        page_size: int = 50
    ) -> List[Dict]:
        """
        获取群聊消息列表

        Args:
            chat_id: 群聊ID
            start_time: 起始时间戳（毫秒）
            end_time: 结束时间戳（毫秒）
            page_size: 每页消息数量

        Returns:
            消息列表
        """
        messages = []
        page_token = None

        # 如果没有指定时间范围，默认获取最近24小时的消息
        if start_time is None:
            start_time = int((datetime.now() - timedelta(days=1)).timestamp() * 1000)
        if end_time is None:
            end_time = int(datetime.now().timestamp() * 1000)

        while True:
            params = {
                "container_id_type": "chat",
                "container_id": chat_id,
                "page_size": page_size,
                "start_time": start_time,
                "end_time": end_time
            }

            if page_token:
                params["page_token"] = page_token

            result = self._request("GET", "/im/v1/messages", params=params)

            items = result.get("data", {}).get("items", [])
            messages.extend(items)

            if not result.get("data", {}).get("has_more"):
                break

            page_token = result.get("data", {}).get("page_token")
            time.sleep(0.5)  # 避免请求过快

        return messages

    def get_user_info(self, user_id: str) -> Dict:
        """
        获取用户信息

        Args:
            user_id: 用户ID

        Returns:
            用户信息
        """
        result = self._request(
            "GET",
            f"/contact/v3/users/{user_id}",
            params={"user_id_type": "user_id"}
        )
        return result.get("data", {}).get("user", {})

    def parse_message_content(self, message: Dict) -> str:
        """
        解析消息内容

        Args:
            message: 消息对象

        Returns:
            解析后的文本内容
        """
        msg_type = message.get("msg_type")
        body = message.get("body", {})
        content = body.get("content", "{}")

        try:
            content_obj = json.loads(content)
        except:
            return content

        if msg_type == "text":
            return content_obj.get("text", "")
        elif msg_type == "post":
            # 富文本消息
            zh_cn = content_obj.get("zh_cn", {})
            title = zh_cn.get("title", "")
            content_list = zh_cn.get("content", [])
            text_parts = []
            for content_item in content_list:
                for item in content_item:
                    if item.get("tag") == "text":
                        text_parts.append(item.get("text", ""))
            return f"{title}\n{''.join(text_parts)}" if title else ''.join(text_parts)
        elif msg_type == "image":
            return "[图片]"
        elif msg_type == "file":
            return f"[文件: {content_obj.get('file_name', '')}]"
        elif msg_type == "audio":
            return "[语音]"
        elif msg_type == "media":
            return "[视频]"
        elif msg_type == "sticker":
            return "[表情]"
        else:
            return f"[{msg_type}]"

    def add_bitable_record(
        self,
        app_token: str,
        table_id: str,
        fields: Dict
    ) -> Dict:
        """
        向多维表格添加记录

        Args:
            app_token: 多维表格app_token
            table_id: 数据表ID
            fields: 字段数据

        Returns:
            创建结果
        """
        endpoint = f"/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        data = {"fields": fields}

        result = self._request("POST", endpoint, json=data)
        return result.get("data", {})

    def batch_add_bitable_records(
        self,
        app_token: str,
        table_id: str,
        records: List[Dict]
    ) -> Dict:
        """
        批量向多维表格添加记录

        Args:
            app_token: 多维表格app_token
            table_id: 数据表ID
            records: 记录列表，每个记录是一个字段字典

        Returns:
            创建结果
        """
        endpoint = f"/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create"
        data = {
            "records": [{"fields": record} for record in records]
        }

        result = self._request("POST", endpoint, json=data)
        return result.get("data", {})
