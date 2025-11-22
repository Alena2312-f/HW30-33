from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Add test users to the database"

    def handle(self, *args, **kwargs):

        # Создание курсов
        user_1 = User.objects.create(email="test.1@mail.ru", city="Москва")
        user_2 = User.objects.create(email="test.22@mail.ru", city="Воронеж")

        self.stdout.write(self.style.SUCCESS(f"Successfully"))
