from django.urls import path
from .views import Login, Signup, Testauth, StopServer

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('signin/', Login.as_view(), name='login'),
    path('test/', Testauth.as_view(), name='testUser'),
    path('stop/', StopServer.as_view(), name='stopserver')
]
