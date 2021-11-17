from rest_framework.serializers import ModelSerializer
from library_of_pantheon_backend.users.models import User, UserSetting

class UserSettingSerializer(ModelSerializer):

    class Meta:
        model = UserSetting
        fields = ("id", "mode", )


class UserSerializer(ModelSerializer):
    setting = UserSettingSerializer(required=False)

    class Meta:
        model = User
        fields = ("id", "name", 'email', "setting", "user_favorites", "username", "password",)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User()
        user.set_password(validated_data['password'])
        validated_data['password'] = user.password
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
