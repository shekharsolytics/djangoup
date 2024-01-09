import requests
import time
import json
import traceback

def _wait_for_user_to_spawn(url, header, jupyter_user, timeout):
    endtime = time.time() + timeout
    while time.time() < endtime:
        r = requests.get(f"{url}hub/api/users/{jupyter_user}", headers=header)
        r.raise_for_status()
        user_model = r.json()

        if "" in user_model["servers"]:
            server_model = user_model["servers"][""]
            if server_model["ready"]:
                return server_model
        else:
            print("Awaiting server info to be part of user_model...")

        time.sleep(1)
    return False

def clone_repository(username, url, github_url, header):
    try:
        url = f"{url}hub/api/users/{username}"
        clone_cmd = ["git", "clone", github_url, f"/opt/bitnami/jupyterhub-singleuser"]
        payload = {"user": username, "cmd": clone_cmd}
        # print(payload)
        response = requests.post(url, headers=header, json=payload)
        print(response)
        # print(response.status)
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        print(e)

