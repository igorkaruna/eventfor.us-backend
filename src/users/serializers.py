from typing import Any, Dict

from django.db.models import Model
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.repositories import UserRepository


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = User
        fields: tuple[str, ...] = ("id", "email", "first_name", "last_name")


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = User
        fields: tuple[str, ...] = ("id", "email", "first_name", "last_name", "password")
        extra_kwargs: Dict[str, Dict[str, Any]] = {"password": {"write_only": True}}

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        for field in ["first_name", "last_name"]:
            if any(char.isdigit() for char in attrs[field]):
                raise serializers.ValidationError({field: "Can only contain alphabet letters"})

        return attrs

    def create(self, validated_data: Dict[str, str]) -> User:
        return UserRepository.create_user(**validated_data)


class UserSignInSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data: Dict[str, Any] = super().validate(attrs)
        data["user"] = {
            "id": str(self.user.id),
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }
        return data


class UserLogoutSerializer(serializers.Serializer):
    refresh_token: str = serializers.CharField()

    @staticmethod
    def validate_refresh_token(value: str) -> str:
        try:
            token = RefreshToken(value)
            token.check_blacklist()
        except TokenError as exc:
            raise serializers.ValidationError(f"Invalid refresh token: {exc}")

        return value
