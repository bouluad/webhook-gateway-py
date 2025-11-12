import requests

def forward_to_jenkins(jenkins_url, payload, event):
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": event,
    }
    response = requests.post(jenkins_url, headers=headers, data=payload, timeout=10)
    return response.status_code
