from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import *

API_router = SimpleRouter()
API_router.register('register', RegisterView, 'register')
API_router.register('user', UserProfile, 'user')
API_router.register('password', ChangePassword, 'password')
API_router.register('change', ChangeUser, 'change')
API_router.register('spider', SpiderView, 'spider')
API_router.register('comment', CommentView, 'comment')
API_router.register('chart', Chart, 'chart')
API_router.register('run', HotListView, 'run'),
API_router.register('screen', Screen, 'screen'),
API_router.register('head', UserImageView, 'head'),

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += API_router.urls
