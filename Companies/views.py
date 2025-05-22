from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import(
    Company,
    WorkDay,
    FirstItem,
    SecondItem,
    CompanyCard,
    CompanyAddress,
    CompanyEmployee,
    CompanyFirstItem,
    CompanySecondItem,
    CompanyValidationStatus,
)
from .serializers import(
    CompanySerializer,
    WorkDaySerializer,
    FirstItemSerializer,
    SecondItemSerializer,
    CompanyCardSerializer,
    CompanyAddressSerializer,
    CompanyEmployeeSerializer,
    CompanyFirstItemSerializer,
    CompanySecondItemSerializer,
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
    


class CompanySecondItemViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing CompanySecondItem instances.
    
    Endpoints:
      - List:      GET /company-second-items/
      - Create:    POST /company-second-items/create/
      - Retrieve:  GET /company-second-items/<slug:slug>/
      - Update:    PUT/PATCH /company-second-items/<slug:slug>/update/
      - Delete:    DELETE /company-second-items/<slug:slug>/delete/
    
    Access for create, update, and delete is restricted to admins or the company’s employer.
    """
    permission_classes = [IsAdminOrCompanyEmployer]

    def list(self, request):
        queryset = CompanySecondItem.objects.all()
        serializer = CompanySecondItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, slug):
        instance = get_object_or_404(CompanySecondItem, slug=slug)
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

    def update(self, request, slug):
        instance = get_object_or_404(CompanySecondItem, slug=slug)
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

    def destroy(self, request, slug):
        instance = get_object_or_404(CompanySecondItem, slug=slug)
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



class CompanyEmployeeViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing CompanyEmployee resources.

    Endpoints:
      - List:      GET /company-employees/
      - Create:    POST /company-employees/create/
      - Retrieve:  GET /company-employees/<pk>/
      - Update:    PUT/PATCH /company-employees/<pk>/update/
      - Delete:    DELETE /company-employees/<pk>/delete/

    Notes:
      • The company is set on create via a write-only field 'company_slug', via which the actual
        Company instance is fetched.
      • On update the company cannot be changed.
      • Permission is enforced via IsAdminOrCompanyEmployer.
    """
    permission_classes = [IsAdminOrCompanyEmployer]

    def list(self, request):
        queryset = CompanyEmployee.objects.all()
        serializer = CompanyEmployeeSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(CompanyEmployee, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = CompanyEmployeeSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = CompanyEmployeeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = CompanyEmployeeSerializer(instance, context={'request': request})
            return Response({
                'message': 'Company employee created successfully.',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        instance = get_object_or_404(CompanyEmployee, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = CompanyEmployeeSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = CompanyEmployeeSerializer(instance, context={'request': request})
            return Response({
                'message': 'Company employee updated successfully.',
                'data': response_serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(CompanyEmployee, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({'message': 'Company employee deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)




class CompanyAddressViewSet(viewsets.ViewSet):
    """
    ViewSet for managing CompanyAddress objects.

    Endpoints:
      - list: GET /company-addresses/
          * If admin, returns all addresses.
          * Otherwise, returns only addresses where company.employer equals request.user.
      - create: POST /company-addresses/create/
          * Creation is allowed only if the request.user equals the company’s employer,
            as validated by the serializer.
      - retrieve: GET /company-addresses/<int:pk>/
          * Access is allowed if the requester is an admin or if the address's company.employer equals request.user.
      - update: PUT/PATCH /company-addresses/<int:pk>/update/
          * Updates are allowed only if request.user matches the company’s employer or is an admin.
      - destroy: DELETE /company-addresses/<int:pk>/delete/
          * Deletion is allowed only if request.user is admin or equals the company’s employer.
    """
    
    permission_classes = [IsAdminOrCompanyEmployer]


    def list(self, request):
        if request.user.is_staff:
            queryset = CompanyAddress.objects.all()
        else:
            queryset = CompanyAddress.objects.filter(company__employer=request.user)
            if not queryset.exists():
                return Response(
                    {"detail": "You do not have permission to view any company address."},
                    status=status.HTTP_403_FORBIDDEN
                )
        serializer = CompanyAddressSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CompanyAddressSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()  # Serializer verifies that request.user == company.employer.
            response_serializer = CompanyAddressSerializer(instance, context={'request': request})
            return Response(
                {"message": "Company address created successfully.", "data": response_serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(CompanyAddress, pk=pk)
        if not (request.user.is_staff or instance.company.employer == request.user):
            return Response(
                {"detail": "You do not have permission to access this company address."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CompanyAddressSerializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_object_or_404(CompanyAddress, pk=pk)
        if not (request.user.is_staff or instance.company.employer == request.user):
            return Response(
                {"detail": "You do not have permission to update this company address."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CompanyAddressSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_instance = serializer.save()
            response_serializer = CompanyAddressSerializer(updated_instance)
            return Response(
                {"message": "Company address updated successfully.", "data": response_serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(CompanyAddress, pk=pk)
        if not (request.user.is_staff or instance.company.employer == request.user):
            return Response(
                {"detail": "You do not have permission to delete this company address."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
        return Response({"message": "Company address deleted."}, status=status.HTTP_204_NO_CONTENT)



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
