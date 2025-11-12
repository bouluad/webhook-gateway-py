from flask import Flask, request, abort
from app.security import verify_signature
from app.router import get_jenkins_url
from app.forwarder import forward_to_jenkins
from app.config import GITHUB_SECRET

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Hub-Signature-256")
    event = request.headers.get("X-GitHub-Event", "unknown")
    payload = request.data

    # 1️⃣ Verify GitHub signature
    if not verify_signature(payload, signature):
        abort(401, "Invalid GitHub signature")

    # 2️⃣ Extract repo/org to decide which Jenkins to use
    data = request.get_json(force=True)
    repo_name = data.get("repository", {}).get("full_name", "")
    if not repo_name:
        abort(400, "Missing repository information")

    jenkins_url = get_jenkins_url(repo_name)
    if not jenkins_url:
        abort(404, f"No Jenkins mapping found for {repo_name}")

    # 3️⃣ Forward the webhook
    status_code = forward_to_jenkins(jenkins_url, payload, event)
    return ("OK", status_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
