from django.urls import path, include
from .routers import CompanyRouter, FirstItemRouter, SecondItemRouter



app_name = "Companies"


company_router = CompanyRouter()
first_item_router = FirstItemRouter()
second_item_router = SecondItemRouter()


urlpatterns = [
    path('company/', include(company_router.get_urls())),
    path('first-item/', include(first_item_router.get_urls())),
    path('second-item/', include(second_item_router.get_urls())),
]