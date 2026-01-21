from flask import Flask, request
import requests
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

FEISHU_WEBHOOK_URL = "你的飞书机器人Webhook地址"

@app.route('/grafana', methods=['POST'])
def grafana_proxy():
    data = request.json
    logging.info("Received Grafana Data: %s", json.dumps(data))

    alerts = data.get('alerts', [])
    for alert in alerts:
        status = alert.get('status', 'unknown')
        labels = alert.get('labels', {})
        annotations = alert.get('annotations', {})

        # 1. 提取基础信息
        summary = annotations.get('summary') or annotations.get('Summary') or "无摘要"
        description = annotations.get('description') or annotations.get('Description') or "无详情"

        # 2. 提取你需要的核心 Labels
        instance = labels.get('instance', '未知实例')
        job = labels.get('job', '未知任务')
        # 磁盘特有的挂载点
        mountpoint = labels.get('mountpoint')

        # 3. 构造展示文本 (Markdown 格式)
        # 使用列表形式展示，更整齐
        info_md = f"**告警实例:** {instance}\n"
        info_md += f"**所属任务:** {job}\n"

        # 如果有挂载点信息，才展示这一行
        if mountpoint:
            info_md += f"**挂载点:** `{mountpoint}`\n"

        info_md += f"**详细详情:** {description}"

        # 4. 构造飞书卡片
        card_content = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": f"【监控告警】{summary}"},
                "template": "red" if status == "firing" else "green"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": info_md
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "note",
                    "elements": [{"tag": "plain_text", "content": f"状态: {status.upper()} | 来源: Grafana"}]
                }
            ]
        }

        # 发送请求
        try:
            resp = requests.post(FEISHU_WEBHOOK_URL, json={
                "msg_type": "interactive",
                "card": card_content
            })
            logging.info("Feishu Response: %s", resp.text)
        except Exception as e:
            logging.error("Send to Feishu failed: %s", str(e))

    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
