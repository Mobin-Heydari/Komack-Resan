from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Company
from .serializers import CompanySerializer
from .permissions import IsAdminOrOwner



class CompanyViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, creating, updating, and deleting Company instances.

    - List: Admin users see all companies; other users see only validated companies.
    - Retrieve: Returns the company by its slug. Non-validated companies are accessible only to staff.
    - Create, Update, Destroy: Restricted to admin users or users with user_type 'OW'.
    """
    permission_classes = [IsAdminOrOwner]

    def list(self, request):
        if request.user.is_staff:
            queryset = Company.objects.all()
        else:
            queryset = Company.objects.filter(is_validated=True)
        serializer = CompanySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, slug):
        company = get_object_or_404(Company, slug=slug)
        if company.is_validated or request.user.is_staff:
            serializer = CompanySerializer(company, context={'request': request})
            return Response(serializer.data)
        return Response(
            {"detail": "You don't have permission to access this company."},
            status=status.HTTP_403_FORBIDDEN
        )

    def create(self, request):
        """
        Create a new company. Only authenticated users with appropriate permissions
        (admin or user_type 'OW') are allowed to create a company.
        """
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication is required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CompanySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            company = serializer.save()
            # Re-serialize the created instance so that we send complete data back.
            response_serializer = CompanySerializer(company, context={'request': request})
            return Response(
                {
                    'message': 'Company created successfully.',
                    'data': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        """
        Update an existing company. Only allowed for admin users or the owner of the company.
        """
        company = get_object_or_404(Company, slug=slug)
        self.check_object_permissions(request, company)
        serializer = CompanySerializer(company, data=request.data, context={'request': request})
        if serializer.is_valid():
            company = serializer.save()
            response_serializer = CompanySerializer(company, context={'request': request})
            return Response(
                {
                    'message': 'Company updated successfully.',
                    'data': response_serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        """
        Delete an existing company. Only allowed for admin users or the owner of the company.
        """
        company = get_object_or_404(Company, slug=slug)
        self.check_object_permissions(request, company)
        company.delete()
        return Response(
            {'message': 'Company deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
