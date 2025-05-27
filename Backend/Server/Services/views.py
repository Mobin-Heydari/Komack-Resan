from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Service, ServicePayment
from .serializers import ServiceSerializer, ServicePaymentSerializer
from .permissions import IsServiceActionAllowed, IsServicePaymentActionAllowed



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


class ServicePaymentViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing ServicePayment records.
    
    Endpoints:
      - List:      GET /service-payments/
      - Create:    POST /service-payments/create/
      - Retrieve:  GET /service-payments/<id>/
      - Update:    PUT/PATCH /service-payments/<id>/update/
      
    Note: The destroy method is not provided.
    """
    permission_classes = [IsServicePaymentActionAllowed]
    lookup_field = 'id'

    def list(self, request):
        queryset = ServicePayment.objects.all()
        serializer = ServicePaymentSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, id=None):
        payment = get_object_or_404(ServicePayment, id=id)
        self.check_object_permissions(request, payment)
        serializer = ServicePaymentSerializer(payment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, id=None):
        payment = get_object_or_404(ServicePayment, id=id)
        self.check_object_permissions(request, payment)
        serializer = ServicePaymentSerializer(payment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            payment = serializer.save()
            response_serializer = ServicePaymentSerializer(payment, context={'request': request})
            return Response({
                'message': 'Payment updated successfully.',
                'data': response_serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
