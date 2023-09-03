from rest_framework import serializers
from ..models import City, PetCategory, Tag, Pet

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("name", "zip_code")

class PetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PetCategory
        fields =  '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'description', 'active')
    
class PetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=160)
    description = serializers.CharField()
    contact_number = serializers.CharField(max_length=15)
    owner = serializers.StringRelatedField(many=False)
    # owner = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Pet
        fields = [
            'id',
            'name',
            'description',
            'contact_number',
            'category',
            'tags',
            'photoUrls',
            'status',
            'owner'
        ]
        extra_kwargs = {'owner': {'read_only': True}}