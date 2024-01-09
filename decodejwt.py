
import jwt
secret_key = 'django-insecure-fs72dabcoo*4ojpu00ewry$7ntui5u3&)x0u^wpqexa9*)%)4f'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzMTkyNzczLCJpYXQiOjE3MDMxODkxNzMsIm51bGwiOiI1Yjc0NzVjN2RkOGI0Zjk5YTI5NzljYzM4MjdjZDBlNiIsImVtYWlsIjoiYmFsZ29wYWwucGF0cm9Ac29seXRpY3MtcGFydG5lcnMuY29tIn0.fYO9HjUUuUSrPGJ5azbXIXA49qFRADOsV_yHi3qdIU4'

decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
username = decoded.get('email')
print(username.split(".")[0])
