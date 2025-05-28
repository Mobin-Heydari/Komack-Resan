from django.urls import path, include
from .routers import ServiceRouter, ServicePaymentRouter



app_name = "Services"


service_router = ServiceRouter()
service_payment_router = ServicePaymentRouter()


urlpatterns = [
    path('service/', include(service_router.get_urls())),
    path('payment/', include(service_payment_router.get_urls())),
]