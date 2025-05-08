from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status

from .models import (
    Company,
)
from .serializers import (
    CompanySerializer,
)


class CompanyViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving Company instances.
    """
    def list(self, request):
        if request.user.is_staff:
            queryset = Company.objects.all()
            serializer = CompanySerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            queryset = Company.objects.filter(is_validated=True)
            serializer = CompanySerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)


    def retrieve(self, request, slug):
        instance = get_object_or_404(Company, slug=slug)
        if instance.is_validated == True or request.user.is_staff:
            serializer = CompanySerializer(instance, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"Error": "You dont have a permission to access."})
