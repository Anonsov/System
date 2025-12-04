import time
import requests
import sys
import os

sys.path.append('/home/anonsina/All/System')  # Path to your Django project root
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'system.settings')  # Or 'system.settings' if lowercase

import django
django.setup()

from apps.runner.base import Runner
from apps.submissions.models import Submission


API = "http://localhost:8000/api/v1"

def main():
    runner = Runner(model=Submission)
    while True:
        
        r = requests.get(f"{API}/submissions/next-pending/")
        if r.status_code == 204:
            time.sleep(4)
            continue


        task = r.json()
        if "id" not in task:
            print("No 'id' in response:", task)
            time.sleep(3)
            continue
        sub_id = task["id"]


        result = runner.run_all_tests(sub_id)
        time.sleep(3)

        # Send results back to the API
        requests.patch(
            f"{API}/submissions/{sub_id}/update/", json={"results": result}
        )
        time.sleep(3)

if __name__ == "__main__":
    main()