# 1. 创建项目目录
mkdir -p /opt/feishu-adapter
cd /opt/feishu-adapter

# 2. 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate
pip install flask requests gunicorn  # 引入 gunicorn 提高并发能力

sudo nano /etc/systemd/system/feishu-adapter.service

[Unit]
Description=Grafana to Feishu Webhook Adapter
After=network.target

[Service]
# 修改为你的实际用户名
User=root
Group=root
WorkingDirectory=/opt/feishu-adapter
# 使用 gunicorn 启动服务，监听 5000 端口
ExecStart=/opt/feishu-adapter/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always
# 默认日志进 systemd journal；如需落文件可加：
# StandardOutput=append:/var/log/feishu-adapter.log
# StandardError=append:/var/log/feishu-adapter.err

[Install]
WantedBy=multi-user.target

# 重新加载配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start feishu-adapter

# 设置开机自启
sudo systemctl enable feishu-adapter

# 查看状态
sudo systemctl status feishu-adapter

# 【调试利器】打印收到的完整 JSON，你可以通过 journalctl -u feishu-adapter -f 查看
# 如果配置了 StandardOutput/StandardError，日志会落到对应文件

# 常用排查命令
# 最近 100 行
journalctl -u feishu-adapter -n 100 --no-pager
# 最近 1 小时
journalctl -u feishu-adapter --since "1 hour ago" --no-pager
# 指定时间范围
journalctl -u feishu-adapter --since "2025-01-01 10:00" --until "2025-01-01 12:00" --no-pager
# 使用 ISO 时间格式输出
journalctl -u feishu-adapter -o short-iso --no-pager
# 按关键字过滤（大小写不敏感）
journalctl -u feishu-adapter --no-pager | grep -i "error"
