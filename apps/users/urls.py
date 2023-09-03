from django.urls import path, re_path
from django.conf.urls import include
from .views import CreateUserView, ActivateUser
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register('users', UserViewSet, basename='users')

app_name = 'users'

urlpatterns = [
    re_path(r'api/', include(router.urls)),
    path('api-register/', CreateUserView.as_view(), name='api-register'),
    re_path(r'api-activate/(?P<token>.+?)/', ActivateUser.as_view(), name='activate'),
]