from django.urls import include, path
from rest_framework import routers
from . import views




class CompanyRouter(routers.DefaultRouter):
    """
    Custom router for CompanyViewSet.
    
    Endpoints under /companies/:
      - List:           GET /companies/
      - Create:         POST /companies/create/
      - Retrieve:       GET /companies/<slug:slug>/
      - Update:         PUT/PATCH /companies/<slug:slug>/
      - Delete:         DELETE /companies/<slug:slug>/
      
    You can easily extend the update route to support additional URL parameters if needed.
    """
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix so that our custom URLs under /companies/ work.
        self.register(r'', views.CompanyViewSet, basename='company')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route: GET /companies/
                path('', views.CompanyViewSet.as_view({'get': 'list'})),
                # Create route: POST /companies/create/
                path('create/', views.CompanyViewSet.as_view({'post': 'create'})),
                # Retrieve, update, and delete using the company slug.
                path('<slug:slug>/', include([
                    # Basic detail route: GET, PUT/PATCH, DELETE.
                    path('', views.CompanyViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'patch': 'update',
                        'delete': 'destroy'
                    })),
                    # Optionally, if ever you need a route with an extra parameter for update
                    # path('<str:extra>/', views.CompanyViewSet.as_view({'put': 'update'})),
                ])),
            ])),
        ]
        return urls + custom_urls



class CompanyValidationStatusRouter(routers.DefaultRouter):
    """
    Custom router for CompanyValidationStatusViewSet.
    
    Endpoints:
      - List:    GET /company-validation-status/
      - Detail:  GET /company-validation-status/<pk>/
      - Update:  PUT/PATCH /company-validation-status/<pk>/
    """
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix to allow custom routes
        self.register(r'', views.CompanyValidationStatusViewSet, basename='company_validation_status')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route: GET /company-validation-status/
                path('', views.CompanyValidationStatusViewSet.as_view({'get': 'list'}),
                     name='company_validation_status-list'),
                # Detail route: Retrieve and Update using the record PK.
                path('<int:pk>/', views.CompanyValidationStatusViewSet.as_view({
                    'get': 'retrieve',
                    'put': 'update',
                    'patch': 'update'
                }), name='company_validation_status-detail'),
            ])),
        ]
        return default_urls + custom_urls



class CompanyFirstItemRouter(routers.DefaultRouter):
    """
    Custom router for CompanyFirstItemViewSet.
    
    Endpoints:
      - List:       GET /company-first-items/
      - Create:     POST /company-first-items/create/
      - Retrieve:   GET /company-first-items/<slug:slug>/
      - Update:     PUT/PATCH /company-first-items/<slug:slug>/update/
      - Delete:     DELETE /company-first-items/<slug:slug>/delete/
    """
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix.
        self.register(r'', views.CompanyFirstItemViewSet, basename='company_first_item')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route
                path('', views.CompanyFirstItemViewSet.as_view({'get': 'list'}), name='company-first-item-list'),
                # Create route
                path('create/', views.CompanyFirstItemViewSet.as_view({'post': 'create'}), name='company-first-item-create'),
                # Detail routes (retrieve, update, delete) using the item slug.
                path('<slug:slug>/', include([
                    path(
                        '',
                        views.CompanyFirstItemViewSet.as_view({
                            'get': 'retrieve',
                            'put': 'update',
                            'patch': 'update',
                            'delete': 'destroy'
                        }),
                        name='company-first-item-detail'
                    ),
                ])),
            ])),
        ]
        return default_urls + custom_urls



class CompanySecondItemRouter(routers.DefaultRouter):
    """
    Custom router for CompanySecondItemViewSet.
    
    Endpoints:
      - List:       GET /company-second-items/
      - Create:     POST /company-second-items/create/
      - Retrieve:   GET /company-second-items/<slug:slug>/
      - Update:     PUT/PATCH /company-second-items/<slug:slug>/update/
      - Delete:     DELETE /company-second-items/<slug:slug>/delete/
    """
    def __init__(self):
        super().__init__()
        self.register(r'', views.CompanySecondItemViewSet, basename='company_second_item')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route
                path('', views.CompanySecondItemViewSet.as_view({'get': 'list'}), name='company-second-item-list'),
                # Create route
                path('create/', views.CompanySecondItemViewSet.as_view({'post': 'create'}), name='company-second-item-create'),
                # Detail routes (retrieve, update, delete) using the item slug.
                path('<slug:slug>/', include([
                    path(
                        '',
                        views.CompanySecondItemViewSet.as_view({
                            'get': 'retrieve',
                            'put': 'update',
                            'patch': 'update',
                            'delete': 'destroy'
                        }),
                        name='company-second-item-detail'
                    ),
                ])),
            ])),
        ]
        return default_urls + custom_urls



class WorkDayRouter(routers.DefaultRouter):
    """
    Custom router for WorkDayViewSet.
    
    Endpoints:
      - List:      GET /workdays/
      - Create:    POST /workdays/create/
      - Retrieve:  GET /workdays/<int:pk>/
      - Update:    PUT/PATCH /workdays/<int:pk>/update/
      - Delete:    DELETE /workdays/<int:pk>/delete/
    """
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix.
        self.register(r'', views.WorkDayViewSet, basename='workday')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route: GET /workdays/
                path('', views.WorkDayViewSet.as_view({'get': 'list'}), name='workday-list'),
                # Create route: POST /workdays/create/
                path('create/', views.WorkDayViewSet.as_view({'post': 'create'}), name='workday-create'),
                # Detail routes for Retrieve, Update, and Delete using pk
                path('<int:pk>/', include([
                    # Retrieve route: GET /workdays/<int:pk>/
                    path('', views.WorkDayViewSet.as_view({
                        'get': 'retrieve'
                    }), name='workday-detail'),
                    # Update route: PUT/PATCH /workdays/<int:pk>/update/
                    path('update/', views.WorkDayViewSet.as_view({
                        'put': 'update',
                        'patch': 'update'
                    }), name='workday-update'),
                    # Delete route: DELETE /workdays/<int:pk>/delete/
                    path('delete/', views.WorkDayViewSet.as_view({
                        'delete': 'destroy'
                    }), name='workday-delete'),
                ])),
            ])),
        ]
        return default_urls + custom_urls



class CompanyCardRouter(routers.DefaultRouter):
    """
    Custom router for CompanyCardViewSet.

    Endpoints:
      - List:       GET    /company-cards/
      - Create:     POST   /company-cards/create/
      - Retrieve:   GET    /company-cards/<int:pk>/
      - Update:     PUT/PATCH /company-cards/<int:pk>/update/
      - Delete:     DELETE /company-cards/<int:pk>/delete/
    """
    def __init__(self):
        super().__init__()
        # Register the CompanyCardViewSet with an empty prefix so that the list endpoint
        # appears at /company-cards/
        self.register(r'', views.CompanyCardViewSet, basename='company_card')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('create/', views.CompanyCardViewSet.as_view({'post': 'create'}), name='company_card-create'),
            path('<int:pk>/', views.CompanyCardViewSet.as_view({'get': 'retrieve'}), name='company_card-detail'),
            path('<int:pk>/update/', views.CompanyCardViewSet.as_view({'put': 'update', 'patch': 'update'}), name='company_card-update'),
            path('<int:pk>/delete/', views.CompanyCardViewSet.as_view({'delete': 'destroy'}), name='company_card-destroy'),
        ]
        return default_urls + custom_urls



class EmployeeRouter(routers.DefaultRouter):
    """
    Custom router for employee viewsets.

    Endpoints under /employees/:

    For Receptionists:
      - List:           GET    /employees/receptionists/
      - Create:         POST   /employees/receptionists/create/
      - Retrieve:       GET    /employees/receptionists/<int:pk>/
      - Update:         PUT/PATCH  /employees/receptionists/<int:pk>/
      - Delete:         DELETE /employees/receptionists/<int:pk>/

    For Accountants:
      - List:           GET    /employees/accountants/
      - Create:         POST   /employees/accountants/create/
      - Retrieve:       GET    /employees/accountants/<int:pk>/
      - Update:         PUT/PATCH  /employees/accountants/<int:pk>/
      - Delete:         DELETE /employees/accountants/<int:pk>/

    For Experts:
      - List:           GET    /employees/experts/
      - Create:         POST   /employees/experts/create/
      - Retrieve:       GET    /employees/experts/<int:pk>/
      - Update:         PUT/PATCH  /employees/experts/<int:pk>/
      - Delete:         DELETE /employees/experts/<int:pk>/
    """
    def __init__(self):
        super().__init__()
        # Register the three viewsets with their respective prefixes.
        self.register(r'receptionists', views.CompanyReceptionistViewSet, basename='receptionist')
        self.register(r'accountants', views.CompanyAccountantViewSet, basename='accountant')
        self.register(r'experts', views.CompanyExpertViewSet, basename='expert')

    def get_urls(self):
        default_urls = super().get_urls()
        # Here we add custom URLs to mirror our style for the companies app.
        custom_urls = [
            path('', include([
                # Receptionists endpoints:
                path('receptionists/', include([
                    # List: GET /employees/receptionists/
                    path('', views.CompanyReceptionistViewSet.as_view({'get': 'list'})),
                    # Create: POST /employees/receptionists/create/
                    path('create/', views.CompanyReceptionistViewSet.as_view({'post': 'create'})),
                    # Retrieve/Update/Delete: /employees/receptionists/<int:pk>/
                    path('<int:pk>/', include([
                        path('', views.CompanyReceptionistViewSet.as_view({
                            'get': 'retrieve',
                            'put': 'update',
                            'patch': 'update',
                            'delete': 'destroy'
                        })),
                    ])),
                ])),
                # Accountants endpoints:
                path('accountants/', include([
                    path('', views.CompanyAccountantViewSet.as_view({'get': 'list'})),
                    path('create/', views.CompanyAccountantViewSet.as_view({'post': 'create'})),
                    path('<int:pk>/', include([
                        path('', views.CompanyAccountantViewSet.as_view({
                            'get': 'retrieve',
                            'put': 'update',
                            'patch': 'update',
                            'delete': 'destroy'
                        })),
                    ])),
                ])),
                # Experts endpoints:
                path('experts/', include([
                    path('', views.CompanyExpertViewSet.as_view({'get': 'list'})),
                    path('create/', views.CompanyExpertViewSet.as_view({'post': 'create'})),
                    path('<int:pk>/', include([
                        path('', views.CompanyExpertViewSet.as_view({
                            'get': 'retrieve',
                            'put': 'update',
                            'patch': 'update',
                            'delete': 'destroy'
                        })),
                    ])),
                ])),
            ])),
        ]
        return default_urls + custom_urls