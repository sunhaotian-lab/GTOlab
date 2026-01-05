#!/usr/bin/env python3
"""
飞书消息追踪器 - 主程序
"""
import argparse
import logging
import sys
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from message_tracker import MessageTracker, load_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_tracker(config, start_time=None, end_time=None):
    """
    执行一次追踪任务

    Args:
        config: 配置字典
        start_time: 起始时间
        end_time: 结束时间
    """
    tracker = MessageTracker(config)
    result = tracker.run(start_time=start_time, end_time=end_time)

    if result['success']:
        logger.info(f"✓ 任务执行成功")
        logger.info(f"  - 处理消息数: {result['total_messages']}")
        logger.info(f"  - 保存记录数: {result['saved_records']}")
    else:
        logger.error(f"✗ 任务执行失败: {result.get('error')}")


def scheduled_job(config):
    """定时任务：追踪前一天的消息"""
    # 获取昨天的日期范围
    yesterday = datetime.now() - timedelta(days=1)
    start_time = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    logger.info(f"定时任务触发: 追踪日期 {start_time.date()}")
    run_tracker(config, start_time, end_time)


def start_scheduler(config):
    """启动定时调度器"""
    schedule_config = config.get('schedule', {})
    run_time = schedule_config.get('run_time', '23:00')
    timezone = schedule_config.get('timezone', 'Asia/Shanghai')

    # 解析运行时间
    hour, minute = run_time.split(':')
    hour = int(hour)
    minute = int(minute)

    # 创建调度器
    scheduler = BlockingScheduler(timezone=pytz.timezone(timezone))

    # 添加定时任务
    scheduler.add_job(
        scheduled_job,
        args=[config],
        trigger=CronTrigger(hour=hour, minute=minute),
        id='message_tracker',
        name='飞书消息追踪',
        replace_existing=True
    )

    logger.info("=" * 60)
    logger.info("定时任务调度器已启动")
    logger.info(f"运行时间: 每天 {run_time} ({timezone})")
    logger.info(f"下次运行: {scheduler.get_jobs()[0].next_run_time}")
    logger.info("按 Ctrl+C 停止")
    logger.info("=" * 60)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("调度器已停止")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='飞书消息追踪器 - 自动追踪群聊消息并保存到多维表格'
    )
    parser.add_argument(
        '--config',
        default='config.json',
        help='配置文件路径（默认: config.json）'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='执行一次任务后退出（默认追踪最近24小时）'
    )
    parser.add_argument(
        '--date',
        help='指定追踪日期（格式: YYYY-MM-DD）'
    )
    parser.add_argument(
        '--start-time',
        help='指定起始时间（格式: YYYY-MM-DD HH:MM:SS）'
    )
    parser.add_argument(
        '--end-time',
        help='指定结束时间（格式: YYYY-MM-DD HH:MM:SS）'
    )

    args = parser.parse_args()

    # 加载配置
    try:
        config = load_config(args.config)
    except Exception as e:
        logger.error(f"加载配置失败: {e}")
        sys.exit(1)

    # 解析时间参数
    start_time = None
    end_time = None

    if args.date:
        # 追踪指定日期
        try:
            date = datetime.strptime(args.date, '%Y-%m-%d')
            start_time = date.replace(hour=0, minute=0, second=0)
            end_time = date.replace(hour=23, minute=59, second=59)
        except ValueError:
            logger.error("日期格式错误，应为: YYYY-MM-DD")
            sys.exit(1)

    if args.start_time:
        try:
            start_time = datetime.strptime(args.start_time, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            logger.error("起始时间格式错误，应为: YYYY-MM-DD HH:MM:SS")
            sys.exit(1)

    if args.end_time:
        try:
            end_time = datetime.strptime(args.end_time, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            logger.error("结束时间格式错误，应为: YYYY-MM-DD HH:MM:SS")
            sys.exit(1)

    # 执行模式
    if args.once:
        # 单次执行模式
        logger.info("单次执行模式")
        run_tracker(config, start_time, end_time)
    else:
        # 定时执行模式
        if args.date or args.start_time or args.end_time:
            logger.warning("定时模式下时间参数将被忽略")
        start_scheduler(config)


if __name__ == '__main__':
    main()
