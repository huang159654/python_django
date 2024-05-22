from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = '__all__'


class ChangeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class TokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["token"] = 'Bearer ' + str(refresh.access_token)
        data['user_id'] = str(self.user.id)
        data['user_name'] = str(self.user.username)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data


class SpiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpiderModel
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class HotListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotListModel
        fields = ['aid', 'owner_name', 'bvid', 'category', 'pub_location',
                  'ctime', 'title', 'tname', 'view', 'danmaku', 'his_rank',
                  'like', 'reply', 'share', 'coin', 'desc']
