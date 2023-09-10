from django.http import Http404
from django.shortcuts import get_object_or_404
from .serializers import CitySerializer, PetCategorySerializer, TagSerializer, PetSerializer
from ..models import City, Tag, PetCategory, Pet
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from .decorators import validate_request_data, IsSeller, IsOwner
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator
####################################
#########  City Viewset  ###########
####################################

class CityViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Company
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin):  # handles GETs for many Companies

    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
####################################
#########  City Views  #############
####################################

class ListCreateCityView(generics.ListCreateAPIView):
    """
    GET cities/
    POST cities/
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        a_song = City.objects.create(
            name=request.data["name"],
            zip_code=request.data["zip_code"]
        )
        return Response(
            data=CitySerializer(a_song).data,
            status=status.HTTP_201_CREATED
        )

class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET city/:id/
    PUT city/:id/
    DELETE city/:id/
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            return Response(CitySerializer(a_song).data)
        except City.DoesNotExist:
            return Response(
                data={
                    "message": "City with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            serializer = CitySerializer()
            updated_song = serializer.update(a_song, request.data)
            return Response(CitySerializer(updated_song).data)
        except City.DoesNotExist:
            return Response(
                data={
                    "message": "City with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            a_song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except City.DoesNotExist:
            return Response(
                data={
                    "message": "City with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

####################################
#########  Category Views  #########
####################################

@api_view(['GET'])
@permission_classes(( IsSeller & permissions.IsAdminUser, ))
def list_category(request):
    categories_list = PetCategory.objects.all()
    paginator = Paginator(categories_list, 20)
    page = request.GET.get('page')
    clinics = paginator.get_page(page)
    page_json = PetCategorySerializer(clinics, many=True)
    return Response(
        data=page_json.data,
        status=status.HTTP_200_OK,
    )

@api_view(['POST'])
@permission_classes((IsSeller & IsOwner, ))
def create_category(request):
    PetCategory.objects.create(
        name=request.data["name"],
        description=request.data["description"],
        active=request.data["active"]
    )
    return Response(
        data={
            "message": "Category created"
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def get_category(request, pk):
    category = get_object_or_404(PetCategory, pk=pk)
    category_json = PetCategorySerializer(category)
    return Response(category_json.data, status=status.HTTP_200_OK)

####################################
#########  Tag Viewset  ############
####################################

class TagViewSet(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 tag
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     ListModelMixin,
                     DestroyModelMixin):  # handles GETs for many tags

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Override the destroy method to set the status to 0
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

####################################
#########  Pets Views  #############
####################################

class RESTPetViewSet(ViewSet):
    """Test API ViewSet.
    def list(self, request)
    def create(self, request)
    def retrieve(self, request, pk=None)
    def update(self, request, pk=None)
    def partial_update(self, request, pk=None)
    def destroy(self, request, pk=None)
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    serializer_class = PetSerializer

    def get_object(self, pk):
        try:
            return Pet.objects.get(pk=pk)
        except Pet.DoesNotExist:
            raise Http404

    def list(self, request):
        """Return all pets"""
        all_pets = Pet.objects.filter(status='1').all()
        serialized_pets = self.serializer_class(all_pets, many=True)
        return Response(serialized_pets.data)

    def create(self, request):
        """Create a new Pet."""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            subscriber_instance = Pet.objects.create(**serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles getting an object by its ID."""
        pet = self.get_object(pk)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handles updating an object."""
        pet = self.get_object(pk)
        serializer = self.serializer_class(pet, data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """Handles updating part of an object."""
        pet = self.get_object(pk)
        serializer = self.serializer_class(
            pet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        pet = self.get_object(pk)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
