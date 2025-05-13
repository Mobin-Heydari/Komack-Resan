from django.urls import path, include
from .routers import PaymentInvoiceRouter
from . import views



app_name = "Payments"



invoice_router = PaymentInvoiceRouter()


urlpatterns = [

    path('invoices/', include(invoice_router.get_urls())),

    path('zarinpal-pay/<str:invoice_id>/', views.SendPaymentRequest.as_view()),
    path('zarinpal-verify/', views.VerifyPaymentRequest.as_view())
]