from django.core.management.base import BaseCommand

from lms.models import Course, Lesson


class Command(BaseCommand):
    help = "Add test courses to the database"

    def handle(self, *args, **kwargs):

        # Создание курсов
        course_1 = Course.objects.create(name="Курс 1", description="Курс 1")
        course_2 = Course.objects.create(name="Курс 2", description="Курс 2")

        self.stdout.write(self.style.SUCCESS(f"Successfully"))
