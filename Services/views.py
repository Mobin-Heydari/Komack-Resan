from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Service, ServiceEmployee
from .serializers import ServiceSerializer, ServiceEmployeeSerializer
from .permissions import IsServiceActionAllowed



class ServiceViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing Service records using slug as lookup.
    
    Endpoints:
      - List:      GET /services/
      - Create:    POST /services/create/
      - Retrieve:  GET /services/<slug>/
      - Update:    PUT/PATCH /services/<slug>/update/
    
    Note: The destroy method is not provided.
    """
    permission_classes = [IsServiceActionAllowed]
    lookup_field = 'slug'

    def list(self, request):
        queryset = Service.objects.all()
        serializer = ServiceSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        service = get_object_or_404(Service, slug=slug)
        self.check_object_permissions(request, service)
        serializer = ServiceSerializer(service, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = ServiceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            service = serializer.save()
            response_serializer = ServiceSerializer(service, context={'request': request})
            return Response({
                'message': 'Service created successfully.',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug=None):
        service = get_object_or_404(Service, slug=slug)
        self.check_object_permissions(request, service)
        serializer = ServiceSerializer(service, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            service = serializer.save()
            response_serializer = ServiceSerializer(service, context={'request': request})
            return Response({
                'message': 'Service updated successfully.',
                'data': response_serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ServiceEmployeeViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing ServiceEmployee records.
    
    Endpoints:
      - List:      GET /service-employees/
      - Create:    POST /service-employees/create/
      - Retrieve:  GET /service-employees/<pk>/
      - Update:    PUT/PATCH /service-employees/<pk>/update/
      - Delete:    DELETE /service-employees/<pk>/delete/
      
    Note: Custom permissions will be integrated later.
    """
    
    permission_classes = []  

    def list(self, request):
        queryset = ServiceEmployee.objects.all()
        serializer = ServiceEmployeeSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(ServiceEmployee, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = ServiceEmployeeSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = ServiceEmployeeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = ServiceEmployeeSerializer(instance, context={'request': request})
            return Response({
                'message': 'Service employee created successfully.',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        instance = get_object_or_404(ServiceEmployee, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = ServiceEmployeeSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = ServiceEmployeeSerializer(instance, context={'request': request})
            return Response({
                'message': 'Service employee updated successfully.',
                'data': response_serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(ServiceEmployee, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({'message': 'Service employee deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
