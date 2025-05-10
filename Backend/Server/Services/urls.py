from django.urls import path, include
from .routers import ServiceRouter



app_name = "Services"


service_router = ServiceRouter()


urlpatterns = [
    path('', include(service_router.get_urls())),
]