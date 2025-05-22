from django.urls import include, path
from rest_framework import routers
from .views import PaymentInvoiceViewSet

class PaymentInvoiceRouter(routers.DefaultRouter):
    """
    Custom router for PaymentInvoiceViewSet.

    Endpoints:
      - List:      GET /payment-invoices/
      - Create:    POST /payment-invoices/create/
      - Retrieve:  GET /payment-invoices/<int:pk>/
      - Update:    PUT/PATCH /payment-invoices/<int:pk>/update/
    """
    def __init__(self):
        super().__init__()
        # Register the PaymentInvoiceViewSet with an empty prefix.
        self.register(r'', PaymentInvoiceViewSet, basename='payment_invoice')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List endpoint: GET /payment-invoices/
                path('', PaymentInvoiceViewSet.as_view({'get': 'list'}), name='payment-invoice-list'),
                # Create endpoint: POST /payment-invoices/create/
                path('create/', PaymentInvoiceViewSet.as_view({'post': 'create'}), name='payment-invoice-create'),
                # Detail endpoints: keyed by primary key.
                path('<int:pk>/', include([
                    # Retrieve endpoint: GET /payment-invoices/<int:pk>/
                    path('', PaymentInvoiceViewSet.as_view({'get': 'retrieve'}), name='payment-invoice-detail'),
                    # Update endpoint: PUT/PATCH /payment-invoices/<int:pk>/update/
                    path('update/', PaymentInvoiceViewSet.as_view({'put': 'update', 'patch': 'update'}), name='payment-invoice-update'),
                ])),
            ])),
        ]
        return default_urls + custom_urls
