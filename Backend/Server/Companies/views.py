from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import(
    Company,
    WorkDay,
    CompanyCard,
    CompanyReceptionist,
    CompanyAccountant,
    CompanyExpert,
    CompanyFirstItem,
    CompanySecondItem,
    CompanyValidationStatus,
)
from .serializers import(
    CompanySerializer,
    WorkDaySerializer,
    CompanyCardSerializer,
    CompanyFirstItemSerializer,
    CompanySecondItemSerializer,
    CompanyValidationStatusSerializer,
    CompanyReceptionistSerializer,
    CompanyAccountantSerializer,
    CompanyExpertSerializer
)
from .permissions import (
    IsAdminOnly,
    IsAdminOrEmployer,
    IsAdminOrCompanyEmployer,
    IsCompanyEmployeeOwnerOrAdmin
)



class CompanyViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing, retrieving, creating, updating, and deleting Company instances.

    - List: Admin users see all companies; other users see only validated companies.
    - Retrieve: Returns the company by its slug. Non-validated companies are accessible only to staff.
    - Create, Update, Destroy: Restricted to admin users or users with user_type 'OW'.
    """
    # permission_classes = [IsAdminOrOwner]
    lookup_field = 'slug'

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
        serializer = CompanySerializer(company, partial=True, data=request.data, context={'request': request})
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
      - Retrieve:  GET /company-first-items/<int:pk>/
      - Update:    PUT/PATCH /company-first-items/<int:pk>/update/
      - Delete:    DELETE /company-first-items/<int:pk>/delete/
    
    Access for write actions (create, update, delete) is restricted to admins or the company’s employer.
    """
    permission_classes = [IsAdminOrCompanyEmployer]

    def list(self, request):
        queryset = CompanyFirstItem.objects.all()
        serializer = CompanyFirstItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        instance = get_object_or_404(CompanyFirstItem, id=pk)
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

    def update(self, request, pk):
        instance = get_object_or_404(CompanyFirstItem, id=pk)
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

    def destroy(self, request, pk):
        instance = get_object_or_404(CompanyFirstItem, id=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response(
            {'message': 'Company first item deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
    


class CompanySecondItemViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing CompanySecondItem instances.
    
    Endpoints:
      - List:      GET /company-second-items/
      - Create:    POST /company-second-items/create/
      - Retrieve:  GET /company-second-items/<int:pk>/
      - Update:    PUT/PATCH /company-second-items/<int:pk>/update/
      - Delete:    DELETE /company-second-items/<int:pk>/delete/
    
    Access for create, update, and delete is restricted to admins or the company’s employer.
    """
    permission_classes = [IsAdminOrCompanyEmployer]

    def list(self, request):
        queryset = CompanySecondItem.objects.all()
        serializer = CompanySecondItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        instance = get_object_or_404(CompanySecondItem, id=pk)
        self.check_object_permissions(request, instance)
        serializer = CompanySecondItemSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = CompanySecondItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = CompanySecondItemSerializer(instance, context={'request': request})
            return Response(
                {
                    'message': 'Company second item created successfully.',
                    'data': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        instance = get_object_or_404(CompanySecondItem, id=pk)
        self.check_object_permissions(request, instance)
        serializer = CompanySecondItemSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = CompanySecondItemSerializer(instance, context={'request': request})
            return Response(
                {
                    'message': 'Company second item updated successfully.',
                    'data': response_serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = get_object_or_404(CompanySecondItem, id=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response(
            {'message': 'Company second item deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )



class WorkDayViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing WorkDay records.
    
    Endpoints:
      - List:      GET /workdays/
      - Create:    POST /workdays/create/
      - Retrieve:  GET /workdays/<pk>/
      - Update:    PUT/PATCH /workdays/<pk>/update/
      - Delete:    DELETE /workdays/<pk>/delete/
    
    Note:
      - The company association must be provided on create via company_slug,
        and cannot be changed on update.
      - The permission class ensures that only admins or the company employer can perform write operations.
    """
    permission_classes = [IsAdminOrCompanyEmployer]

    def list(self, request):
        queryset = WorkDay.objects.all()
        serializer = WorkDaySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        workday = get_object_or_404(WorkDay, pk=pk)
        self.check_object_permissions(request, workday)
        serializer = WorkDaySerializer(workday, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = WorkDaySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            workday = serializer.save()
            response_serializer = WorkDaySerializer(workday, context={'request': request})
            return Response(
                {
                    'message': 'Workday created successfully.',
                    'data': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        workday = get_object_or_404(WorkDay, pk=pk)
        self.check_object_permissions(request, workday)
        serializer = WorkDaySerializer(workday, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            workday = serializer.save()
            response_serializer = WorkDaySerializer(workday, context={'request': request})
            return Response(
                {
                    'message': 'Workday updated successfully.',
                    'data': response_serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        workday = get_object_or_404(WorkDay, pk=pk)
        self.check_object_permissions(request, workday)
        workday.delete()
        return Response(
            {'message': 'Workday deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )



class CompanyCardViewSet(viewsets.ViewSet):
    """
    ViewSet for managing CompanyCard objects.

    Endpoints:
        - list: GET /company-cards/
            • If request.user is admin, returns all company cards.
            • Otherwise, returns only the card for companies where the user is the employer.
        - create: POST /company-cards/create/
            • Only allowed if request.user is admin or matches company.employer.
        - retrieve: GET /company-cards/<pk>/
            • Only allowed if request.user is admin or matches the card's company employer.
        - update: PUT/PATCH /company-cards/<pk>/update/
            • Only allowed if request.user is admin or matches the card's company employer.
        - destroy: DELETE /company-cards/<pk>/delete/
            • Only allowed if request.user is admin or matches the card's company employer.
    """

    permission_classes = [IsAdminOrCompanyEmployer]
    
    def list(self, request):
        if request.user.is_staff:
            queryset = CompanyCard.objects.all()
        else:
            queryset = CompanyCard.objects.filter(company__employer=request.user)
            if not queryset.exists():
                return Response(
                    {"detail": "No company card found for your company."},
                    status=status.HTTP_404_NOT_FOUND
                )
        serializer = CompanyCardSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = CompanyCardSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            card = serializer.save()
            response_serializer = CompanyCardSerializer(card, context={'request': request})
            return Response(
                {
                    "message": "Company card created successfully.",
                    "data": response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        card = get_object_or_404(CompanyCard, pk=pk)
        # Only admin or company employer can access.
        if not request.user.is_staff and card.company.employer != request.user:
            return Response(
                {"detail": "You do not have permission to access this company card."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CompanyCardSerializer(card, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        card = get_object_or_404(CompanyCard, pk=pk)
        # Only admin or company employer can update.
        if not request.user.is_staff and card.company.employer != request.user:
            return Response(
                {"detail": "You do not have permission to update this company card."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CompanyCardSerializer(card, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_card = serializer.save()
            response_serializer = CompanyCardSerializer(updated_card, context={'request': request})
            return Response(
                {
                    "message": "Company card updated successfully.",
                    "data": response_serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        card = get_object_or_404(CompanyCard, pk=pk)
        # Only admin or company employer can delete.
        if not request.user.is_staff and card.company.employer != request.user:
            return Response(
                {"detail": "You do not have permission to delete this company card."},
                status=status.HTTP_403_FORBIDDEN
            )
        card.delete()
        return Response(
            {"message": "Company card deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class CompanyReceptionistViewSet(viewsets.ViewSet):
    """
    ViewSet for managing Company Receptionist records.
    
    List:
      - If 'company_slug' query parameter is provided, filter by that.
      - Non-admin users (company owner with user type OW) only see records for companies they own.
    
    Retrieve:
      - Accessible if the request user is admin, or if the user is the record's employee,
        or if the user is the company employer.
    
    Create, Update, Destroy:
      - Only allowed if the user is admin or if the user is the company employer.
    """
    permission_classes = [IsAuthenticated, IsCompanyEmployeeOwnerOrAdmin]

    def list(self, request):
        qs = CompanyReceptionist.objects.all()
        company_slug = request.query_params.get('company_slug')
        user = request.user

        if company_slug:
            qs = qs.filter(company__slug=company_slug)
        else:
            if not user.is_staff:
                qs = qs.filter(company__employer=user)
        serializer = CompanyReceptionistSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(CompanyReceptionist, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = CompanyReceptionistSerializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = CompanyReceptionistSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer = CompanyReceptionistSerializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = get_object_or_404(CompanyReceptionist, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = CompanyReceptionistSerializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer = CompanyReceptionistSerializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(CompanyReceptionist, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({"detail": "Record deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class CompanyAccountantViewSet(viewsets.ViewSet):
    """
    ViewSet for managing Company Accountant records.
    """
    permission_classes = [IsAuthenticated, IsCompanyEmployeeOwnerOrAdmin]

    def list(self, request):
        qs = CompanyAccountant.objects.all()
        company_slug = request.query_params.get('company_slug')
        user = request.user

        if company_slug:
            qs = qs.filter(company__slug=company_slug)
        else:
            if not user.is_staff:
                qs = qs.filter(company__employer=user)
        serializer = CompanyAccountantSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(CompanyAccountant, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = CompanyAccountantSerializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = CompanyAccountantSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer = CompanyAccountantSerializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = get_object_or_404(CompanyAccountant, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = CompanyAccountantSerializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        serializer = CompanyAccountantSerializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(CompanyAccountant, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({"detail": "Record deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
