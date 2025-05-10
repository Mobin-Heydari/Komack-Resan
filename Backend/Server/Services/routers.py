from django.urls import include, path
from rest_framework import routers
from .views import ServiceViewSet

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
                path('create/', ServiceViewSet.as_view({'post': 'create'}), name='service-create'),
                # Detail routes using slug.
                path('<slug:slug>/', include([
                    # Retrieve route: GET /services/<slug>/
                    path('', ServiceViewSet.as_view({'get': 'retrieve'}), name='service-detail'),
                    # Update route: PUT/PATCH /services/<slug>/update/
                    path('update/', ServiceViewSet.as_view({'put': 'update', 'patch': 'update'}), name='service-update'),
                ])),
            ])),
        ]
        return default_urls + custom_urls
