import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')

import django

django.setup()

from django.contrib.auth.models import User

username = 'testuser'
password = 'TestPass123!'

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User',
    },
)

user.set_password(password)
user.save()

print(f'{username}:{password}:{"created" if created else "updated"}')
