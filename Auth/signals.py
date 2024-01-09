import requests
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_jupyterhub_user(sender, instance, created, **kwargs):

    if created:
        # jupyter_hub_url = "http://192.168.49.2:32611/hub/api"
        # token = "295e178df69a47568630cca7379aa3d5"
        jupyter_hub_url = "https://nimbus-dev-jupyterhub.solytics.us/hub/api"
        token = "e695520948124cb99e844427d96de4b1"
        headers = {
            'Authorization': f'token {token}'
        }
        response = requests.post(f"{jupyter_hub_url}/users/{instance.username}", headers=headers)
        print(response.json())