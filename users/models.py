from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatars", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    payment_date = models.DateField()
    paid_course = models.ForeignKey(
        "lms.Course",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments",
    )
    paid_lesson = models.ForeignKey(
        "lms.Lesson",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments",
    )
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
        ("stripe", "Stripe"),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    stripe_checkout_session_id = models.CharField(
        max_length=255, blank=True, null=True
    )  # ID сессии
    payment_url = models.URLField(
        blank=True, null=True
    )  # Добавляем поле для URL оплаты
    is_paid = models.BooleanField(default=False)  # Поле для статуса оплаты

    def __str__(self):
        return f"Payment by {self.user} on {self.payment_date}"


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        "lms.Course", on_delete=models.CASCADE, related_name="subscriptions"
    )

    class Meta:
        unique_together = (
            "user",
            "course",
        )  # Один пользователь может подписаться на курс только один раз

    def __str__(self):
        return f"Subscription: {self.user} -> {self.course}"