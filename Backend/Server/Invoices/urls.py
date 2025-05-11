from django.urls import path, include

from .routers import InvoiceRouter




app_name = "Invoices"


invoice_router = InvoiceRouter()


urlpatterns = [
    path('', include(invoice_router.get_urls())),
]