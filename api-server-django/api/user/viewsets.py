from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.user.models import User
from api.user.permissions import IsSuperUser
from api.user.serializers import UserAdminUpdateSerializer, UserSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    queryset = User.objects.all().order_by("username")
    permission_classes = (IsSuperUser,)
    http_method_names = ["get", "patch"]

    def get_serializer_class(self):
        if self.action == "partial_update":
            return UserAdminUpdateSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"success": True, "users": serializer.data})

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.pk == request.user.pk:
            raise ValidationError({"success": False, "msg": "You cannot change your own account here."})

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"success": True, "user": UserSerializer(instance).data}, status=status.HTTP_200_OK)
