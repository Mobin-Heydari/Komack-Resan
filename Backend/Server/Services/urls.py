from django.urls import path, include
from .routers import ServiceRouter, ServiceEmployeeRouter



app_name = "Services"


service_router = ServiceRouter()
service_employee_router = ServiceEmployeeRouter()


urlpatterns = [
    path('service/', include(service_router.get_urls())),
    path('employee/', include(service_employee_router.get_urls())),
]