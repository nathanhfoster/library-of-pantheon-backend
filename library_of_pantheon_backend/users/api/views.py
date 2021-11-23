from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import update_last_login
from rest_framework import generics
from library_of_pantheon_backend.users.models import User, UserSetting
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserSettingSerializer
from library_of_pantheon_backend.utils.pagination import StandardResultsSetPagination


def get_user_response(token, user):
    update_last_login(None, user)
    user_setting = UserSettingSerializer(user.setting).data
    return {
        'token': token.key,
        'id': user.pk,
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'setting': user_setting,
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'last_login': user.last_login,
        'date_joined': user.date_joined,
    }


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class RegisterViewSet(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response(get_user_response(token, user))


class LoginViewSet(ObtainAuthToken):
    permission_classses = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = get_object_or_404(Token, user=user)
        return Response(get_user_response(token, user))


class UpdateSettingsViewSet(generics.UpdateAPIView):
    queryset = UserSetting.objects.all()
    serializer_class = UserSettingSerializer
