from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.urls import app_name

from lms import views
from lms.apps import LmsConfig
from lms.views import LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"courses", views.CourseViewSet, basename="course")

urlpatterns = [
    path("courses/", include(router.urls)),
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson-list-create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyAPIView.as_view(),
        name="lesson-retrieve-update-destroy",
    ),
]

urlpatterns += router.urls
