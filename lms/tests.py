# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson

User = get_user_model()


class CourseTests(APITestCase):
    def setUp(self):
        # Создаем тест user
        self.user = User.objects.create(email="test@example.com", password="testpassword")
        # Создаем тест course
        self.course = Course.objects.create(name="Test Course", description="Test Description", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_list(self):
        url = reverse("lms:course-list")  # Используйте имя, которое вы указали в urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # дописать нужно


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com", password="testpassword")
        self.course = Course.objects.create(name="Test Course", description="Test Description", owner=self.user)

    def test_subscription_create(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("lms:subscription")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")

    def test_subscription_delete(self):
        # Сначала создайте подписку
        self.client.force_authenticate(user=self.user)
        url = reverse("lms:subscription")
        data = {"course_id": self.course.id}
        self.client.post(url, data)

        # Затем удалите его
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")


class LessonTests(APITestCase):
    def setUp(self):
        # Создаем тест user
        self.user = User.objects.create(email="test@example.com", password="testpassword")
        # Создаем тест course
        self.course = Course.objects.create(name="Test Course", description="Test Description", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Test Lesson", description="Test Lesson", owner=self.user, course_id=self.course.pk
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        url = reverse("lms:lesson-list-create")  # Используйте имя, которое вы указали в urls.py
        response = self.client.get(url)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create(self):
        url = reverse("lms:lesson-list-create")  # Используйте имя, которое вы указали в urls.py
        data = {
            "owner": self.user.pk,
            "course": self.course.pk,
            "name": "Test Lesson 2",
            "description": "Test Lesson 2",
            "video_link": "https://www.youtube.com/",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_retrieve(self):
        url = reverse(
            "lms:lesson-retrieve-update-destroy", args=(self.lesson.pk,)
        )  # Используйте имя, которое вы указали в urls.py
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Test Lesson")

    def test_lesson_update(self):
        url = reverse(
            "lms:lesson-retrieve-update-destroy", args=(self.lesson.pk,)
        )  # Используйте имя, которое вы указали в urls.py
        data = {"name": "Test Lesson2"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Test Lesson2")

    def test_lesson_delete(self):
        url = reverse(
            "lms:lesson-retrieve-update-destroy", args=(self.lesson.pk,)
        )  # Используйте имя, которое вы указали в urls.py
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)
