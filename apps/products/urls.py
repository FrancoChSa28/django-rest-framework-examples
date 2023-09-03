from django.urls import path, re_path
from .views import CustomerDetail, CustomerList, ProductDetail, ProductList

urlpatterns = [
    re_path(r'^customers/(?P<id>\d+)$', CustomerDetail.as_view(), name='customer-detail'),
    re_path(r'^customers/$', CustomerList.as_view(), name='customer-list'),
    re_path(r'^customers/(?P<customer_id>\d+)/favorite-products/$', ProductList.as_view(), name='customer-favorite-product-list'),
    re_path(r'^customers/(?P<customer_id>\d+)/favorite-products/(?P<id>\d+)$', ProductDetail.as_view(), name='customer-favorite-product-detail'),
]
