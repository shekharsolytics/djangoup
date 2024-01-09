import requests
import subprocess
import time
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from Auth.utility import _wait_for_user_to_spawn, clone_repository

# jupyterhub_url = "http://192.168.49.2:32611/"
# token = "295e178df69a47568630cca7379aa3d5"

jupyterhub_url = "https://nimbus-dev-jupyterhub.solytics.us/"
token = "e695520948124cb99e844427d96de4b1"
headers = {'Authorization': f'token {token}'}
timeout = 50

github_url = "https://github.com/Subhasish-Halder/sum.git"



class Signup(APIView):

    @staticmethod
    def post(request):
        data = request.data

        username = data['username']
        password = data['password']
        email = data['email']

        user = User.objects.create(username=username, password=make_password(password), email=email)
        return Response(data = {"msg": f"user created, id: {user.id}"}, status=201)

class Login(APIView):

    @staticmethod
    def post(request):
        data = request.data
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={"token": token.key}, status=200)
        else:
            return Response(data={"error": "Invalid user credentials."}, status=401)



class Testauth(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        username = request.user.username
        response = requests.post(
            f"{jupyterhub_url}hub/api/users/{username}/server",
            headers=headers
        )

        if response.status_code in (201, 202):
            try:
                # check successfull spawn
                server_model = _wait_for_user_to_spawn(
                    jupyterhub_url, headers, username, timeout
                )
                if server_model:
                    print(server_model)
                    pod_name = server_model["state"]["pod_name"]
                    namespace = server_model["state"]["namespace"]
                    # c = subprocess.run(
                    #     [
                    #         "kubectl",
                    #         "exec",
                    #         f"--namespace={namespace}",
                    #         pod_name,
                    #         "--",
                    #         "sh",
                    #         "-c",
                    #         "if [ -z $TEST_ENV_FIELDREF_TO_NAMESPACE ]; then exit 1; fi",
                    #     ]
                    # )
                    # clone_repository(username, jupyterhub_url, github_url ,headers)
                    
                    notebook_url = f"{jupyterhub_url}user/{username}/"
                    return HttpResponseRedirect(notebook_url)
                    return Response(data={"msg": "data done"}, status=200)
                return Response(data={"msg": "timeout"}, status=400)
            except Exception as e:
                
                print(e)
                return Response(data={"msg": f"{e}"}, status=400)

        return Response(data={"error": f"Unable to spawn notebook."}, status=response.status_code)

class StopServer(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        username = request.user.username
        response = requests.delete(
            f"{jupyterhub_url}hub/api/users/{username}/server",
            headers=headers
        )
        if response.status_code in (202, 204):
            endtime = time.time() + timeout
            while time.time() < endtime:
                r = requests.get(f"{jupyterhub_url}hub/api/users/{username}", headers=headers)
                r.raise_for_status()
                user_model = r.json()
                print(user_model)
                if "" not in user_model["servers"]:
                    return Response(data={"message": "server stopped"}, status=204)
                time.sleep(1)
            return Response(data={"message": "timeout"}, status=400)
        return Response(data={"message": "Server Not running"}, status=response.status_code)