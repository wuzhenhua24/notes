# app.py
from flask import Flask, request
import requests
import json

app = Flask(__name__)

# 配置你的飞书机器人 Webhook 地址
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx-xxxx"

@app.route('/grafana', methods=['POST'])
def grafana_proxy():
    data = request.json
    # 提取 Grafana 告警核心信息
    alerts = data.get('alerts', [])
    for alert in alerts:
        status = alert.get('status', 'unknown')
        summary = alert.get('annotations', {}).get('summary', '无摘要')
        description = alert.get('annotations', {}).get('description', '无详情')

        # 构造飞书卡片消息
        card_content = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": f"【Grafana】{status.upper()}"},
                "template": "red" if status == "firing" else "green"
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**告警摘要:** {summary}"}},
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**详细描述:** {description}"}},
                {"tag": "note", "elements": [{"tag": "plain_text", "content": "来自监控中心"}]}
            ]
        }

        # 发送给飞书
        requests.post(FEISHU_WEBHOOK_URL, json={
            "msg_type": "interactive",
            "card": card_content
        })
    return "ok", 200

# 你可以继续添加 /jenkins, /prometheus 等路由来适配其他应用
@app.route('/other', methods=['POST'])
def other_proxy():
    # 逻辑类似，根据其他应用的 JSON 结构做转换
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
