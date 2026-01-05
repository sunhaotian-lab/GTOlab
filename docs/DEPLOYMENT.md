# 部署指南

本文档介绍如何将飞书消息追踪器部署到不同的环境中，实现24小时自动运行。

## 部署方式选择

| 部署方式 | 优点 | 缺点 | 适用场景 |
|---------|------|------|---------|
| 本地电脑 | 简单，免费 | 需要电脑一直开机 | 测试、短期使用 |
| 云服务器 | 稳定，24小时运行 | 需要费用 | 长期使用 |
| Docker | 易于管理和迁移 | 需要了解Docker | 容器化部署 |
| 云函数 | 按需付费，免运维 | 有冷启动时间 | 定时任务 |

## 方式一：本地电脑部署

### Windows

#### 1. 安装Python

下载并安装 Python 3.8+ : https://www.python.org/downloads/

#### 2. 设置开机自启动

创建批处理文件 `start_tracker.bat`:

```batch
@echo off
cd /d C:\path\to\GTOlab
python main.py
```

将该文件添加到启动文件夹：
- 按 `Win+R`
- 输入 `shell:startup`
- 将批处理文件复制到打开的文件夹

### macOS

#### 1. 创建启动服务

创建文件 `~/Library/LaunchAgents/com.feishu.tracker.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.feishu.tracker</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/GTOlab/main.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/GTOlab</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

#### 2. 加载服务

```bash
launchctl load ~/Library/LaunchAgents/com.feishu.tracker.plist
```

### Linux

#### 1. 创建systemd服务

创建文件 `/etc/systemd/system/feishu-tracker.service`:

```ini
[Unit]
Description=Feishu Message Tracker
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/GTOlab
ExecStart=/usr/bin/python3 /path/to/GTOlab/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 2. 启动服务

```bash
# 重载systemd配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start feishu-tracker

# 设置开机自启
sudo systemctl enable feishu-tracker

# 查看状态
sudo systemctl status feishu-tracker

# 查看日志
sudo journalctl -u feishu-tracker -f
```

## 方式二：云服务器部署

推荐的云服务器提供商：
- 阿里云
- 腾讯云
- AWS
- 华为云

### 1. 购买服务器

最低配置建议：
- CPU: 1核
- 内存: 1GB
- 操作系统: Ubuntu 20.04 或 CentOS 7+

### 2. 连接服务器

```bash
ssh root@your-server-ip
```

### 3. 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
# sudo yum update -y  # CentOS

# 安装Python3和pip
sudo apt install python3 python3-pip git -y  # Ubuntu/Debian
# sudo yum install python3 python3-pip git -y  # CentOS
```

### 4. 部署应用

```bash
# 克隆代码
cd /opt
git clone <your-repo-url> GTOlab
cd GTOlab

# 安装依赖
pip3 install -r requirements.txt

# 配置
cp config.example.json config.json
nano config.json  # 编辑配置文件
```

### 5. 使用systemd管理（参考Linux部署步骤）

### 6. 配置防火墙（如需要）

```bash
# 如果需要开放端口（本应用不需要）
sudo ufw allow 22  # SSH
sudo ufw enable
```

## 方式三：Docker部署

### 1. 创建Dockerfile

创建文件 `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 运行
CMD ["python", "main.py"]
```

### 2. 创建docker-compose.yml

```yaml
version: '3.8'

services:
  tracker:
    build: .
    container_name: feishu-tracker
    restart: unless-stopped
    volumes:
      - ./config.json:/app/config.json:ro
      - ./logs:/app/logs
    environment:
      - TZ=Asia/Shanghai
```

### 3. 部署

```bash
# 构建镜像
docker-compose build

# 启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

## 方式四：云函数部署（高级）

### 腾讯云函数

#### 1. 修改代码适配云函数

创建 `scf_main.py`:

```python
import json
from datetime import datetime, timedelta
from message_tracker import MessageTracker

def main_handler(event, context):
    """云函数入口"""
    # 加载配置（从环境变量或对象存储）
    config = {
        "feishu": {
            "app_id": os.environ.get('APP_ID'),
            "app_secret": os.environ.get('APP_SECRET')
        },
        "tracker": {
            "chat_id": os.environ.get('CHAT_ID'),
            "target_user_id": os.environ.get('TARGET_USER_ID'),
            "bitable_app_token": os.environ.get('BITABLE_APP_TOKEN'),
            "bitable_table_id": os.environ.get('BITABLE_TABLE_ID')
        }
    }

    # 执行追踪
    yesterday = datetime.now() - timedelta(days=1)
    start_time = yesterday.replace(hour=0, minute=0, second=0)
    end_time = yesterday.replace(hour=23, minute=59, second=59)

    tracker = MessageTracker(config)
    result = tracker.run(start_time=start_time, end_time=end_time)

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }
```

#### 2. 创建云函数

1. 登录腾讯云控制台
2. 进入云函数服务
3. 创建函数，选择Python 3.7运行环境
4. 上传代码（打包为zip）
5. 配置环境变量
6. 设置定时触发器

### 阿里云函数计算

类似腾讯云，需要适配阿里云的函数入口格式。

## 监控和维护

### 日志管理

#### 1. 添加文件日志

修改 `main.py`，添加文件日志处理器：

```python
import logging
from logging.handlers import RotatingFileHandler

# 添加文件日志
file_handler = RotatingFileHandler(
    'logs/tracker.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logging.getLogger().addHandler(file_handler)
```

#### 2. 日志轮转

使用logrotate（Linux）：

创建 `/etc/logrotate.d/feishu-tracker`:

```
/opt/GTOlab/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

### 健康检查

创建 `health_check.py`:

```python
#!/usr/bin/env python3
"""健康检查脚本"""
import os
import sys
from datetime import datetime

LOG_FILE = "logs/tracker.log"
MAX_HOURS = 25  # 超过25小时没有日志则告警

if not os.path.exists(LOG_FILE):
    print("ERROR: Log file not found")
    sys.exit(1)

# 检查最后修改时间
last_modified = os.path.getmtime(LOG_FILE)
hours_ago = (datetime.now().timestamp() - last_modified) / 3600

if hours_ago > MAX_HOURS:
    print(f"WARNING: No log updates in {hours_ago:.1f} hours")
    sys.exit(1)
else:
    print(f"OK: Last update {hours_ago:.1f} hours ago")
    sys.exit(0)
```

设置定时健康检查（crontab）：

```bash
# 每小时检查一次
0 * * * * /usr/bin/python3 /opt/GTOlab/health_check.py || echo "Tracker health check failed" | mail -s "Alert" your@email.com
```

### 告警配置

可以集成以下告警方式：
1. 邮件告警
2. 飞书机器人消息
3. 短信告警
4. 监控平台（如：Prometheus + Grafana）

## 安全建议

1. **保护配置文件**
   ```bash
   chmod 600 config.json
   ```

2. **使用环境变量**
   不要将敏感信息硬编码，使用环境变量：
   ```python
   import os
   app_id = os.environ.get('FEISHU_APP_ID')
   ```

3. **定期更新**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

4. **备份配置**
   定期备份配置文件和数据

5. **网络安全**
   - 使用防火墙限制访问
   - 定期更新系统补丁

## 性能优化

### 1. 减少API调用

缓存用户信息：

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_user_info_cached(self, user_id):
    return self.client.get_user_info(user_id)
```

### 2. 批量处理

已实现批量写入多维表格，无需优化。

### 3. 异步处理（高级）

使用异步HTTP库提升性能：

```bash
pip install aiohttp
```

## 故障恢复

### 1. 数据库记录

记录已处理的消息ID，避免重复：

```python
# 使用SQLite记录处理状态
import sqlite3

def is_processed(message_id):
    # 检查是否已处理
    pass

def mark_processed(message_id):
    # 标记为已处理
    pass
```

### 2. 重试机制

代码中已包含基本重试，可以增强：

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_with_retry():
    # 会自动重试
    pass
```

## 总结

根据你的需求选择合适的部署方式：

- **测试/个人使用**: 本地部署
- **生产环境**: 云服务器 + Docker
- **轻量级定时任务**: 云函数
- **高可用**: 云服务器 + 监控 + 告警

祝你部署顺利！
