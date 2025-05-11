from django.urls import path, include
from .routers import PaymentInvoiceRouter



app_name = "Payments"



invoice_router = PaymentInvoiceRouter()


urlpatterns = [
    path('invoices/', include(invoice_router.get_urls())),
]