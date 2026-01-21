{{ define "feishu_msg" }}
{
  "msg_type": "text",
  "content": {
    "text": "【Grafana 报警通知】\n状态: {{ .Status | upper }}\n内容: {{ range .Alerts }}{{ .Annotations.summary }}\n详情: {{ .Annotations.description }}\n时间: {{ .StartsAt.Format "2006-01-02 15:04:05" }}\n{{ end }}"
  }
}
{{ end }}
