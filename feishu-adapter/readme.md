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
