"""
飞书消息追踪器
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List
from feishu_client import FeishuClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MessageTracker:
    """消息追踪器"""

    def __init__(self, config: Dict):
        """
        初始化消息追踪器

        Args:
            config: 配置字典
        """
        self.config = config
        self.client = FeishuClient(
            app_id=config['feishu']['app_id'],
            app_secret=config['feishu']['app_secret']
        )

        self.chat_id = config['tracker']['chat_id']
        self.target_user_id = config['tracker']['target_user_id']
        self.bitable_app_token = config['tracker']['bitable_app_token']
        self.bitable_table_id = config['tracker']['bitable_table_id']

    def fetch_user_messages(
        self,
        start_time: datetime = None,
        end_time: datetime = None
    ) -> List[Dict]:
        """
        获取目标用户的消息

        Args:
            start_time: 起始时间，默认为24小时前
            end_time: 结束时间，默认为当前时间

        Returns:
            消息列表
        """
        if start_time is None:
            start_time = datetime.now() - timedelta(days=1)
        if end_time is None:
            end_time = datetime.now()

        start_timestamp = int(start_time.timestamp() * 1000)
        end_timestamp = int(end_time.timestamp() * 1000)

        logger.info(f"开始获取消息: {start_time} - {end_time}")

        try:
            all_messages = self.client.get_chat_messages(
                chat_id=self.chat_id,
                start_time=start_timestamp,
                end_time=end_timestamp
            )

            logger.info(f"获取到 {len(all_messages)} 条消息")

            # 筛选目标用户的消息
            user_messages = []
            for msg in all_messages:
                sender_id = msg.get("sender", {}).get("id")
                if sender_id == self.target_user_id:
                    user_messages.append(msg)

            logger.info(f"筛选出目标用户的 {len(user_messages)} 条消息")
            return user_messages

        except Exception as e:
            logger.error(f"获取消息失败: {e}")
            raise

    def parse_messages_to_records(self, messages: List[Dict]) -> List[Dict]:
        """
        将消息解析为多维表格记录格式

        Args:
            messages: 消息列表

        Returns:
            记录列表
        """
        records = []

        for msg in messages:
            try:
                # 获取消息时间
                create_time = int(msg.get("create_time", 0))
                dt = datetime.fromtimestamp(create_time / 1000)

                # 解析消息内容
                content = self.client.parse_message_content(msg)

                # 获取发送者信息
                sender = msg.get("sender", {})
                sender_id = sender.get("id", "")

                # 尝试获取用户名（如果之前没有缓存，可能需要调用API）
                try:
                    user_info = self.client.get_user_info(sender_id)
                    user_name = user_info.get("name", sender_id)
                except:
                    user_name = sender_id

                # 构建记录
                record = {
                    "日期": dt.strftime("%Y-%m-%d"),
                    "时间": dt.strftime("%H:%M:%S"),
                    "用户名": user_name,
                    "消息内容": content,
                    "消息类型": msg.get("msg_type", "unknown"),
                    "消息ID": msg.get("message_id", "")
                }

                records.append(record)

            except Exception as e:
                logger.warning(f"解析消息失败: {e}, 消息ID: {msg.get('message_id')}")
                continue

        return records

    def save_to_bitable(self, records: List[Dict]) -> bool:
        """
        保存记录到多维表格

        Args:
            records: 记录列表

        Returns:
            是否成功
        """
        if not records:
            logger.info("没有记录需要保存")
            return True

        logger.info(f"准备保存 {len(records)} 条记录到多维表格")

        try:
            # 批量添加记录（飞书API单次最多500条）
            batch_size = 500
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                result = self.client.batch_add_bitable_records(
                    app_token=self.bitable_app_token,
                    table_id=self.bitable_table_id,
                    records=batch
                )
                logger.info(f"成功保存第 {i//batch_size + 1} 批，共 {len(batch)} 条记录")

            logger.info(f"所有记录保存完成")
            return True

        except Exception as e:
            logger.error(f"保存到多维表格失败: {e}")
            raise

    def run(
        self,
        start_time: datetime = None,
        end_time: datetime = None
    ) -> Dict:
        """
        执行一次完整的追踪任务

        Args:
            start_time: 起始时间
            end_time: 结束时间

        Returns:
            执行结果统计
        """
        logger.info("=" * 60)
        logger.info("开始执行消息追踪任务")
        logger.info("=" * 60)

        try:
            # 1. 获取消息
            messages = self.fetch_user_messages(start_time, end_time)

            # 2. 解析消息
            records = self.parse_messages_to_records(messages)

            # 3. 保存到多维表格
            self.save_to_bitable(records)

            result = {
                "success": True,
                "total_messages": len(messages),
                "saved_records": len(records),
                "start_time": start_time.isoformat() if start_time else None,
                "end_time": end_time.isoformat() if end_time else None
            }

            logger.info("=" * 60)
            logger.info(f"任务执行完成: 共处理 {len(messages)} 条消息，保存 {len(records)} 条记录")
            logger.info("=" * 60)

            return result

        except Exception as e:
            logger.error(f"任务执行失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }


def load_config(config_path: str = "config.json") -> Dict:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径

    Returns:
        配置字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logger.error(f"配置文件不存在: {config_path}")
        logger.error("请复制 config.example.json 为 config.json 并填写配置")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"配置文件格式错误: {e}")
        raise
