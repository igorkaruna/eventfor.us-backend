from typing import Any, Dict

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, Token

from users.repositories import UserRepository


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        for field in ["first_name", "last_name"]:
            if any(char.isdigit() for char in attrs[field]):
                raise serializers.ValidationError({field: "Can only contain alphabet letters"})

        return attrs

    def create(self, validated_data: Dict[str, Any]) -> User:
        return UserRepository.create_user(**validated_data)


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    @staticmethod
    def validate_refresh_token(value: Token) -> Token:
        try:
            RefreshToken(value).check_blacklist()
        except TokenError as exc:
            raise serializers.ValidationError(f"Invalid refresh token: {exc}")

        return value
