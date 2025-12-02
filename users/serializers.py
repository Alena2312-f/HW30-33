from rest_framework import serializers
from rest_framework_simplejwt.serializers import AuthUser, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from users.models import Payment, Subscription, User


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)  # Добавляем поле платежей

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "phone",
            "city",
            "avatar",
            "first_name",
            "last_name",
            "payments",
        ]
        extra_kwargs = {"password": {"write_only": True, "required": False}}  # Пароль только для записи

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)  # Хэшируем пароль
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password is not None:
            instance.set_password(password)  # Хэшируем пароль
        return super().update(instance, validated_data)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

    def validate(self, data):
        user = data.get("user")
        course = data.get("course")

        if not user or not course:
            raise serializers.ValidationError("Both user and course are required.")

        # Проверьте, существует ли уже подписка
        if Subscription.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("This subscription already exists.")

        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)

        token["email"] = user.email
        token["first_name"] = user.first_name

        return token


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "email", "first_name", "last_name", "phone", "city", "avatar"]


class PaymentStatusResponse(serializers.Serializer):
    status = serializers.CharField(help_text="Статус платежа в Stripe")
    payment_id = serializers.IntegerField(help_text="ID платежа в системе")
