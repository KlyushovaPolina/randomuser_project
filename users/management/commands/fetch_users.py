from django.core.management.base import BaseCommand
from users.models import User
import requests

class Command(BaseCommand):
    help = 'Fetch users from randomuser.me'

    def handle(self, *args, **kwargs):
        url = 'https://randomuser.me/api/?results=1000'
        response = requests.get(url)
        data = response.json()['results']

        for item in data:
            User.objects.create(
                gender=item['gender'],
                first_name=item['name']['first'],
                last_name=item['name']['last'],
                phone=item['phone'],
                email=item['email'],
                location=", ".join([item['location']['city'], item['location']['country']]),
                picture=item['picture']['thumbnail']
            )
        self.stdout.write(self.style.SUCCESS('Successfully loaded 1000 users'))