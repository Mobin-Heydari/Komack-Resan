from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import FirstItem, SecondItem
from .serializers import FirstItemSerializer, SecondItemSerializer
from .permissions import IsAdminOrReadOnly




class FirstItemViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing FirstItem instances.
    - Listing: Available to all users.
    - Retrieve: Available to all users.
    - Create, Update, Delete: Restricted to admin users.
    """
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    def list(self, request):
        queryset = FirstItem.objects.all()
        serializer = FirstItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, slug):
        first_item = get_object_or_404(FirstItem, slug=slug)
        serializer = FirstItemSerializer(first_item, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = FirstItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            first_item = serializer.save()
            response_serializer = FirstItemSerializer(first_item, context={'request': request})
            return Response(
                {
                    'message': 'FirstItem created successfully.',
                    'data': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        first_item = get_object_or_404(FirstItem, slug=slug)
        self.check_object_permissions(request, first_item)
        serializer = FirstItemSerializer(first_item, data=request.data, context={'request': request})
        if serializer.is_valid():
            first_item = serializer.save()
            response_serializer = FirstItemSerializer(first_item, context={'request': request})
            return Response(
                {
                    'message': 'FirstItem updated successfully.',
                    'data': response_serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        first_item = get_object_or_404(FirstItem, slug=slug)
        self.check_object_permissions(request, first_item)
        first_item.delete()
        return Response(
            {'message': 'FirstItem deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )



class SecondItemViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing SecondItem instances.
    - Listing: Available to all users.
    - Retrieve: Available to all users.
    - Create, Update, Delete: Restricted to admin users.
    """
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    def list(self, request):
        queryset = SecondItem.objects.all()
        serializer = SecondItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, slug):
        second_item = get_object_or_404(SecondItem, slug=slug)
        serializer = SecondItemSerializer(second_item, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = SecondItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            second_item = serializer.save()
            response_serializer = SecondItemSerializer(second_item, context={'request': request})
            return Response(
                {
                    'message': 'SecondItem created successfully.',
                    'data': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        second_item = get_object_or_404(SecondItem, slug=slug)
        self.check_object_permissions(request, second_item)
        serializer = SecondItemSerializer(second_item, data=request.data, context={'request': request})
        if serializer.is_valid():
            second_item = serializer.save()
            response_serializer = SecondItemSerializer(second_item, context={'request': request})
            return Response(
                {
                    'message': 'SecondItem updated successfully.',
                    'data': response_serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        second_item = get_object_or_404(SecondItem, slug=slug)
        self.check_object_permissions(request, second_item)
        second_item.delete()
        return Response(
            {'message': 'SecondItem deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
