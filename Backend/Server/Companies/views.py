from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import(
    Company,
    FirstItem,
    SecondItem,
    CompanyFirstItem,
    CompanyValidationStatus,
)
from .serializers import(
    CompanySerializer,
    FirstItemSerializer,
    SecondItemSerializer,
    CompanyFirstItemSerializer,
    CompanyValidationStatusSerializer,
)
from .permissions import (
    IsAdminOnly,
    IsAdminOrOwner,
    IsAdminOrReadOnly,
    IsAdminOrEmployer,
    IsAdminOrCompanyEmployer,
)



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



class FirstItemViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing FirstItem instances.
    - Listing: Available to all users.
    - Retrieve: Available to all users.
    - Create, Update, Delete: Restricted to admin users.
    """
    permission_classes = [IsAdminOrReadOnly]

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



class CompanyValidationStatusViewSet(viewsets.ViewSet):
    """
    A viewset for listing, retrieving, and updating CompanyValidationStatus instances.
    
    - List: Accessible only by admin; returns all statuses.
    - Retrieve/Update: Accessible by admin or the company employer.
    """
    def get_queryset(self):
        return CompanyValidationStatus.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            # Only admin can list.
            return [IsAdminOnly()]
        elif self.action in ['retrieve', 'update']:
            # For detail and update, allow admin or company owner.
            return [IsAdminOrEmployer()]
        return []

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CompanyValidationStatusSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(CompanyValidationStatus, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = CompanyValidationStatusSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_object_or_404(CompanyValidationStatus, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = CompanyValidationStatusSerializer(
            instance,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CompanyFirstItemViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing CompanyFirstItem instances.
    
    Endpoints:
      - List:      GET /company-first-items/
      - Create:    POST /company-first-items/create/
      - Retrieve:  GET /company-first-items/<slug:slug>/
      - Update:    PUT/PATCH /company-first-items/<slug:slug>/update/
      - Delete:    DELETE /company-first-items/<slug:slug>/delete/
    
    Access for write actions (create, update, delete) is restricted to admins or the company’s employer.
    """
    permission_classes = [IsAdminOrCompanyEmployer]

    def list(self, request):
        queryset = CompanyFirstItem.objects.all()
        serializer = CompanyFirstItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, slug):
        instance = get_object_or_404(CompanyFirstItem, slug=slug)
        self.check_object_permissions(request, instance)
        serializer = CompanyFirstItemSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = CompanyFirstItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = CompanyFirstItemSerializer(instance, context={'request': request})
            return Response(
                {
                    'message': 'Company first item created successfully.',
                    'data': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug):
        instance = get_object_or_404(CompanyFirstItem, slug=slug)
        self.check_object_permissions(request, instance)
        serializer = CompanyFirstItemSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = CompanyFirstItemSerializer(instance, context={'request': request})
            return Response(
                {
                    'message': 'Company first item updated successfully.',
                    'data': response_serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug):
        instance = get_object_or_404(CompanyFirstItem, slug=slug)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response(
            {'message': 'Company first item deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )