import yaml
from app.config import JENKINS_MAP_FILE

def load_map():
    with open(JENKINS_MAP_FILE, "r") as f:
        return yaml.safe_load(f)

def get_jenkins_url(repo_name):
    config = load_map()
    for key, url in config.items():
        if repo_name.startswith(key):
            return url
    return None
