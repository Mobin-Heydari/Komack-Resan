from django.urls import include, path
from rest_framework import routers
from .views import ServiceViewSet, ServiceEmployeeViewSet

class ServiceRouter(routers.DefaultRouter):
    """
    Custom router for ServiceViewSet.
    
    Endpoints:
      - List:      GET /services/
      - Create:    POST /services/create/
      - Retrieve:  GET /services/<slug>/
      - Update:    PUT/PATCH /services/<slug>/update/
    """
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix.
        self.register(r'', ServiceViewSet, basename='service')
    
    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route: GET /services/
                path('', ServiceViewSet.as_view({'get': 'list'}), name='service-list'),
                # Create route: POST /services/create/
                path('', ServiceViewSet.as_view({'post': 'create'}), name='service-create'),
                # Detail routes using slug.
                path('<slug:slug>/', include([
                    # Retrieve route: GET /services/<slug>/
                    path('', ServiceViewSet.as_view({'get': 'retrieve'}), name='service-detail'),
                    # Update route: PUT/PATCH /services/<slug>/update/
                    path('', ServiceViewSet.as_view({'put': 'update', 'patch': 'update'}), name='service-update'),
                ])),
            ])),
        ]
        return default_urls + custom_urls



class ServiceEmployeeRouter(routers.DefaultRouter):
    """
    Custom router for ServiceEmployeeViewSet.
    
    Endpoints:
      - List:      GET /service-employees/
      - Create:    POST /service-employees/create/
      - Retrieve:  GET /service-employees/<int:pk>/
      - Update:    PUT/PATCH /service-employees/<int:pk>/update/
      - Delete:    DELETE /service-employees/<int:pk>/delete/
    """
    
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix.
        self.register(r'', ServiceEmployeeViewSet, basename='service_employee')
    
    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List: GET /service-employees/
                path('', ServiceEmployeeViewSet.as_view({'get': 'list'}), name='service-employee-list'),
                # Create: POST /service-employees/create/
                path('', ServiceEmployeeViewSet.as_view({'post': 'create'}), name='service-employee-create'),
                # Detail routes grouped under the primary key.
                path('<int:pk>/', include([
                    # Retrieve: GET /service-employees/<int:pk>/
                    path('', ServiceEmployeeViewSet.as_view({'get': 'retrieve'}), name='service-employee-detail'),
                    # Update: PUT/PATCH /service-employees/<int:pk>/update/
                    path('', ServiceEmployeeViewSet.as_view({'put': 'update', 'patch': 'update'}), name='service-employee-update'),
                    # Delete: DELETE /service-employees/<int:pk>/delete/
                    path('', ServiceEmployeeViewSet.as_view({'delete': 'destroy'}), name='service-employee-delete'),
                ])),
            ])),
        ]
        return default_urls + custom_urls