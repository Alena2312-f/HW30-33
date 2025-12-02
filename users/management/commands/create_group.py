from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from lms.models import Course, Lesson


class Command(BaseCommand):
    help = "Create product moderator group and assign permissions"

    def handle(self, *args, **kwargs):
        # Создание группы
        moderator_group, created = Group.objects.get_or_create(name="Модератор продуктов")

        # Получение прав
        content_type = ContentType.objects.get_for_model(Lesson, Course)
        can_view = Permission.objects.get(codename="can_view", content_type=content_type)
        update = Permission.objects.get(codename="update", content_type=content_type)

        # Назначение прав группе
        moderator_group.permissions.add(can_view, update)

        self.stdout.write(self.style.SUCCESS("Successfully created product moderator group and assigned permissions"))
