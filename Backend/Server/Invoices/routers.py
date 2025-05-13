from django.urls import include, path
from rest_framework import routers
from .views import InvoiceViewSet

class InvoiceRouter(routers.DefaultRouter):
    """
    Custom router for InvoiceViewSet.

    Endpoints:
      - List:      GET /invoices/
      - Retrieve:  GET /invoices/<int:pk>/
      - Update:    PUT/PATCH /invoices/<int:pk>/update/
    """
    def __init__(self):
        super().__init__()
        self.register(r'', InvoiceViewSet, basename='invoice')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            # Use an include to group custom endpoints
            path('', include([
                # List endpoint: GET /invoices/
                path('', InvoiceViewSet.as_view({'get': 'list'}), name='invoice-list'),
                path('', InvoiceViewSet.as_view({'post': 'create'}), name='invoice-create'),
                # Detail endpoints, keyed by primary key.
                path('<str:pk>/', include([
                    # Retrieve endpoint: GET /invoices/<str:pk>/
                    path('', InvoiceViewSet.as_view({'get': 'retrieve'}), name='invoice-detail'),
                    # Update endpoint: PUT/PATCH /invoices/<str:pk>/update/
                    path('update/', InvoiceViewSet.as_view({'put': 'update', 'patch': 'update'}), name='invoice-update'),
                ]))
            ]))
        ]
        return default_urls + custom_urls
