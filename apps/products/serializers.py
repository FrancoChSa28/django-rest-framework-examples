from .models import Product, Customer
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'customer': {
                'write_only': True
            }
        }

class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'product_id',
            'product_title',
            'product_price',
            'product_image',
            'review_score',
            'created_at',
            'updated_at'
        ]
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'created_at': {
                'read_only': True
            },
            'updated_at': {
                'read_only': True
            },
            'review_score': {
                'required': False
            }
        }

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'
