from django.urls import include, path
from rest_framework import routers
from .views import ServicePaymentViewSet, ServiceViewSet



class ServiceRouter(routers.DefaultRouter):
    """
    Custom router for ServiceViewSet.
    
    Endpoints:
      - List:      GET /services/
      - Create:    POST /services/create/
      - Retrieve:  GET /services/<id>/
      - Update:    PUT/PATCH /services/<id>/update/
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
                # Detail routes using id.
                path('<uuid:id>/', include([
                    # Retrieve route: GET /services/<id>/
                    path('', ServiceViewSet.as_view({'get': 'retrieve'}), name='service-detail'),
                    # Update route: PUT/PATCH /services/<id>/update/
                    path('', ServiceViewSet.as_view({'put': 'update', 'patch': 'update'}), name='service-update'),
                ])),
            ])),
        ]
        return default_urls + custom_urls
    



class ServicePaymentRouter(routers.DefaultRouter):
    """
    Custom router for ServicePaymentViewSet.
    
    Endpoints:
      - List:      GET /service-payments/
      - Retrieve:  GET /service-payments/<int:id>/
      - Update:    PUT/PATCH /service-payments/<int:id>/update/
    """
    
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix so our custom URLs work under /service-payments/
        self.register(r'', ServicePaymentViewSet, basename='service-payment')
    
    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route: GET /service-payments/
                path('', ServicePaymentViewSet.as_view({'get': 'list'}), name='service-payment-list'),
                # Detail routes using the uuid id as lookup.
                path('<uuid:service_id>/', include([
                    # Retrieve route: GET /service-payments/<uuid:service_id>/
                    path('', ServicePaymentViewSet.as_view({'get': 'retrieve'}), name='service-payment-detail'),
                    # Update route: PUT/PATCH /service-payments/<uuid:service_id>/update/
                    path('update/', ServicePaymentViewSet.as_view({'put': 'update', 'patch': 'update'}), name='service-payment-update'),
                ])),
            ])),
        ]
        return default_urls + custom_urls
