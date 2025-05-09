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



class FirstItemRouter(routers.DefaultRouter):
    """
    Custom router for FirstItemViewSet.
    
    Endpoints under the base URL:
      - List:           GET /firstitems/
      - Create:         POST /firstitems/create/
      - Retrieve:       GET /firstitems/<slug:slug>/
      - Update:         PUT/PATCH /firstitems/<slug:slug>/
      - Delete:         DELETE /firstitems/<slug:slug>/
    """
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix.
        self.register(r'', views.FirstItemViewSet, basename='firstitem')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route: GET /firstitems/
                path('', views.FirstItemViewSet.as_view({'get': 'list'}), name='firstitem-list'),
                # Create route: POST /firstitems/create/
                path('create/', views.FirstItemViewSet.as_view({'post': 'create'}), name='firstitem-create'),
                # Detail routes: Retrieve, Update (PUT/PATCH), and Delete using the item slug.
                path('<slug:slug>/', include([
                    path('', views.FirstItemViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'patch': 'update',
                        'delete': 'destroy'
                    }), name='firstitem-detail'),
                ])),
            ])),
        ]
        return default_urls + custom_urls



class SecondItemRouter(routers.DefaultRouter):
    """
    Custom router for SecondItemViewSet.
    
    Endpoints under the base URL:
      - List:           GET /seconditems/
      - Create:         POST /seconditems/create/
      - Retrieve:       GET /seconditems/<slug:slug>/
      - Update:         PUT/PATCH /seconditems/<slug:slug>/
      - Delete:         DELETE /seconditems/<slug:slug>/
    """
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix.
        self.register(r'', views.SecondItemViewSet, basename='seconditem')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route: GET /seconditems/
                path('', views.SecondItemViewSet.as_view({'get': 'list'}), name='seconditem-list'),
                # Create route: POST /seconditems/create/
                path('create/', views.SecondItemViewSet.as_view({'post': 'create'}), name='seconditem-create'),
                # Detail routes: Retrieve, update and delete using the item slug.
                path('<slug:slug>/', include([
                    path('', views.SecondItemViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'patch': 'update',
                        'delete': 'destroy'
                    }), name='seconditem-detail'),
                ])),
            ])),
        ]
        return default_urls + custom_urls



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
