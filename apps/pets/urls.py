from django.urls import path, re_path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .api import viewsets

app_name = 'pets'

router = DefaultRouter(trailing_slash=False)
router.register("cities", viewsets.CityViewSet, basename='city')
router.register("tags", viewsets.TagViewSet, basename='tags')
router.register("pets", viewsets.RESTPetViewSet, basename='pets')

urlpatterns = [
    re_path(r'api/', include(router.urls)),
    # Cities
    re_path(r'^city/$', viewsets.ListCreateCityView.as_view(), name='cities-list-create'),
    re_path(r'^city/(?P<pk>\d+)/$', viewsets.CityDetailView.as_view(), name="cities-detail"),
    # Categories
    path('category/<int:pk>/', viewsets.get_category),
    path('category/list/', viewsets.list_category),
    path('category/create/', viewsets.create_category),
    # Tags
]