class CreateUserAndCloneRepo(ModelAPIView):
    """Create user and clone Git repository"""

    def post(self, request):
        username = request.query_params.get("username")
        repo_url = "https://github.com/Subhasish-Halder/sum"
        create_user_response = self.create_user(username)
        if create_user_response.status_code // 100 == 2:
            workspace_url = create_user_response.json().get('url')
            print(f"workspace_url: {workspace_url}")
            auto_u_part = self.generate_auto_u_part(username)
            print(f"auto_u_part: {auto_u_part}")
            target_workspace = f"https://nimbus-dev-jupyterhub.solytics.us{workspace_url}/lab/workspaces/{auto_u_part}"
            clone_repo_response = self.clone_repository(repo_url, target_workspace)
            if clone_repo_response["status"] == "success":
                return Response({"status": "success", "message": "User created and repository cloned successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "error", "message": "Failed to clone repository", "details": clone_repo_response["details"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"status": "error", "message": "Failed to create user"}, status=create_user_response.status_code)
    
    def generate_auto_u_part(self, username):
        return f"auto-{username}"

    def create_user(self, username):
        hub_api_url = "https://nimbus-dev-jupyterhub.solytics.us/hub/api"
        admin_token = "e695520948124cb99e844427d96de4b1"
        headers = {'Authorization': f'token {admin_token}'}
        create_user_url = f"{hub_api_url}/users/{username}"
        response = requests.post(create_user_url, headers=headers)
        return response

    def clone_repository(self, repo_url, target_workspace):
        try:
            repo = git.Repo.clone_from(repo_url, target_workspace, branch='main')
            print(repo)
            return {"status": "success", "details": f"Repository cloned to {target_workspace}"}
        except Exception as e:
            return {"status": "error", "details": str(e)}