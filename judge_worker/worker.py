import time
import requests

API = "localhost:8000/api/v1"


def run_in_docker(code, language):
    return {
        "status": "AC",
        "output": "",
        "time": 0.01,
        "memory": 10000
    }

def main():
    while True:
        r = requests.get(f"{API}/submissions/next-pending/")
        if r.status_code == 204:
            time.sleep(2)
            continue
        
        task = r.json()
        sub_id = task["id"]
        code = task["code"]
        language = task["language"]
        
        result = run_in_docker(code, language)
        
        requests.post(
            f"{API}/submissions/{sub_id}/update/", json=result
        )
        
        time.sleep(0.5)