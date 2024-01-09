from jupyterhub.auth import LocalAuthenticator
import jwt

secret_key = "django-insecure-fs72dabcoo*4ojpu00ewry$7ntui5u3&)x0u^wpqexa9*)%)4f"

class CustomJWTAuthenticator(LocalAuthenticator):
    def decode_token(self, token):
        return jwt.decode(token, secret_key, algorithms=['HS256'])

    async def authenticate(self, handler, data):
        # token = data.get('Authorization')
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzMTc1MjUzLCJpYXQiOjE3MDMxNzE2NTMsIm51bGwiOiJjMThkMTkwYTU3MWU0ODU0OTJmNjgyZjNlNjZkNjM1MCIsImVtYWlsIjoiYmFsZ29wYWwucGF0cm9Ac29seXRpY3MtcGFydG5lcnMuY29tIn0.BIQHYmzkvR8inbBjHg6Oh-ATq_sH5mD-YcjYj0Y5xzY'
        if not token:
            return None

        try:
            decoded = self.decode_token(token)
            username = decoded.get('username')
            return username
        except jwt.InvalidTokenError:
            return None