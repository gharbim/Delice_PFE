from api.user.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "is_superuser", "date"]
        read_only_field = ["id"]


class UserAdminUpdateSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active"]
        read_only_fields = ["id", "username", "email"]
