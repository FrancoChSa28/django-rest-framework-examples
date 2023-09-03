from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from .models import Customer, Product
from .serializers import CustomerSerializer, ProductSerializer, ProductDetailSerializer
from requests import exceptions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from apps.utils.CustomPagination import CustomPagination
# Create your views here.

#########################################
#####           Customer         ########
#########################################

# Used for read-write endpoints to represent a collection of model instances.
class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]

# Used for read-write-delete endpoints to represent a single model instance.
class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    authentication_classes = [TokenAuthentication]

#########################################
#####           Product          ########
#########################################
class ProductList(generics.ListCreateAPIView):

    lookup_field = 'customer_id'
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    authentication_classes = [TokenAuthentication]
    pagination_class = CustomPagination

    def get_queryset(self):
        customer_id = self.kwargs.get('customer_id')
        if not Customer.objects.filter(id=customer_id).exists():
            raise Http404()

        return Product.objects.filter(
            customer=customer_id
        )

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response(
                {
                    'product_id': [
                        'This field is required.'
                    ]
                },
                status.HTTP_400_BAD_REQUEST
            )

        # try:
        #     product = Product.objects.get(pk=product_id)
        # except exceptions.HTTPError as e:
        #     exception_message = str(e)
        #     status_code = e.response.status_code
        #     if status_code == status.HTTP_404_NOT_FOUND:
        #         exception_message = 'The requested Product doesn’t exist.'
        #         status_code = status.HTTP_400_BAD_REQUEST

        #     return Response(
        #         {
        #             'detail': exception_message
        #         },
        #         status_code
        #     )
        # except Exception as e:
        #     return Response(
        #         None,
        #         status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )

        # if not product:
        #     return Response(
        #         None,
        #         status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )
        
        customer_favorite_product_data = {
            'customer': kwargs.get('customer_id'),
            'product_id': request.data.get('product_id'),
            'product_title': request.data.get('product_title'),
            'product_price': request.data.get('product_price'),
            'product_image': request.data.get('product_image'),
            'review_score': request.data.get('review_score', None),
        }

        serializer = ProductSerializer(data=customer_favorite_product_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'id'
    serializer_class = ProductDetailSerializer
    permission_classes = (IsAdminUser, DjangoModelPermissions)
    authentication_classes = [TokenAuthentication]
    

    def get_queryset(self):
        customer_favorite_product_id = self.kwargs.get('id')
        customer_id = self.kwargs.get('customer_id')

        customer_favorite_product = Product.objects.filter(
            customer=customer_id,
            id=customer_favorite_product_id
        )

        if not customer_favorite_product:
            raise Http404()

        return customer_favorite_product