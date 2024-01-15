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

    
def check_jupyterhub_status(url, header, jupyter_user):
    r = requests.get(f"{url}hub/api/users/{jupyter_user}", headers=header)
    r.raise_for_status()
    user_model = r.json()

    if "" in user_model["servers"]:
        server_model = user_model["servers"][""]
        if server_model["ready"]:
            return True
    return False
