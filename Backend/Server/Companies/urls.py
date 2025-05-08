from django.urls import path, include
from .routers import CompanyRouter



app_name = "Companies"


company_router = CompanyRouter()


urlpatterns = [
    path('', include(company_router.get_urls())),
]