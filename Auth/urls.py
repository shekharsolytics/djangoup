from django.urls import path
from .views import Login, Signup, StartJupyterhubServer, SpawnJupyterhubServer, AccessJupyterhubServer, StopJupyterhubServer

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('signin/', Login.as_view(), name='login'),
    path('hub/start/', StartJupyterhubServer.as_view(), name='startjupyterhub'),
    path('hub/spawn/', SpawnJupyterhubServer.as_view(), name='spawnjupyterhub'),
    path('hub/access/', AccessJupyterhubServer.as_view(), name='accessjupyterhub'),
    path('hub/stop/', StopJupyterhubServer.as_view(), name='stopjupyterhub')
]
