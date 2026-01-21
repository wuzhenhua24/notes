from flask import Flask, request
import requests
import json
import logging

app = Flask(__name__)

# 配置日志，方便在终端看到收到的原始数据
logging.basicConfig(level=logging.INFO)

FEISHU_WEBHOOK_URL = "你的飞书机器人Webhook地址"

@app.route('/grafana', methods=['POST'])
def grafana_proxy():
    data = request.json

    # 【调试利器】打印收到的完整 JSON，你可以通过 journalctl -u feishu-adapter -f 查看
    logging.info("Received Grafana Data: %s", json.dumps(data))

    alerts = data.get('alerts', [])
    for alert in alerts:
        status = alert.get('status', 'unknown')
        annotations = alert.get('annotations', {})

        # 兼容性处理：尝试获取小写或大写的键
        summary = annotations.get('summary') or annotations.get('Summary') or "未定义摘要"
        description = annotations.get('description') or annotations.get('Description') or "未定义详情"

        # 构造飞书卡片
        card_content = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": f"【监控报警】状态: {status.upper()}"},
                "template": "red" if status == "firing" else "green"
            },
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**告警项目:** {summary}"}},
                {"tag": "div", "text": {"tag": "lark_md", "content": f"**详情描述:** {description}"}},
                {"tag": "hr"},
                {"tag": "note", "elements": [{"tag": "plain_text", "content": "数据来源: Grafana 监控系统"}]}
            ]
        }

        requests.post(FEISHU_WEBHOOK_URL, json={
            "msg_type": "interactive",
            "card": card_content
        })
    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
