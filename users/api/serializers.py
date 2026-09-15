from rest_framework import serializers

from users.models import CustomUser
from users.services import UserService


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        style={
            "input_type": "password"
        }
    )

    class Meta:

        model = CustomUser

        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "password",
        )

    def create(self, validated_data):

        return UserService.create_user(
            **validated_data
        )


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomUser

        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "role",
            "created_at",
        )

        read_only_fields = fields

