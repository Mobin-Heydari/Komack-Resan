from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Province, City, RecipientAddress
from .serializers import ProvinceSerializer, CitySerializer, RecipientAddressSerializer
from .permissions import CityProvinceAdminPermission, RecipientAddressPermission





# ------------------------------------------------------------------
# Province ViewSet
# ------------------------------------------------------------------
class ProvinceViewSet(viewsets.ViewSet):
    """
    ViewSet for managing Province objects.

    Endpoints:
      - list:     GET /provinces/
      - create:   POST /provinces/create/           (Admin only)
      - retrieve: GET /provinces/<pk>/
      - update:   PUT/PATCH /provinces/<pk>/update/   (Admin only)
      - destroy:  DELETE /provinces/<pk>/delete/       (Admin only)
    """
    permission_classes = [CityProvinceAdminPermission]

    def list(self, request):
        queryset = Province.objects.all()
        serializer = ProvinceSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = ProvinceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = ProvinceSerializer(instance, context={'request': request})
            return Response(
                {"message": "Province created successfully.", "data": response_serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(Province, pk=pk)
        serializer = ProvinceSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_object_or_404(Province, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = ProvinceSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_instance = serializer.save()
            response_serializer = ProvinceSerializer(updated_instance, context={'request': request})
            return Response(
                {"message": "Province updated successfully.", "data": response_serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(Province, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({"message": "Province deleted."}, status=status.HTTP_204_NO_CONTENT)
