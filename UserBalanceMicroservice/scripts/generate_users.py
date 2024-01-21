import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UserBalanceMicroservice.settings')
django.setup()

from django.contrib.auth.models import User
from faker import Faker

fake = Faker()


def create_users(n):
    for _ in range(n):
        name = fake.name().split()
        user = User.objects.create_user(
            username=fake.user_name(),
            first_name=name[0],
            last_name=name[1],
            email=fake.email(),
            password='123456'
        )
        user.save()
        print(f"Created user {user.username}")


if __name__ == "__main__":
    create_users(5)
