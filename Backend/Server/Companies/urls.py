from django.urls import path, include
from .routers import (
    CompanyRouter,
    WorkDayRouter,
    CompanyCardRouter,
    CompanyAddressRouter,
    CompanyEmployeeRouter,
    CompanyFirstItemRouter,
    CompanySecondItemRouter,
    CompanyValidationStatusRouter,
)



app_name = "Companies"


company_router = CompanyRouter()
company_validation_router = CompanyValidationStatusRouter()
company_first_item_router = CompanyFirstItemRouter()
company_second_item_router = CompanySecondItemRouter()
workday_router = WorkDayRouter()
company_employee_router = CompanyEmployeeRouter()
company_address_router = CompanyAddressRouter()
company_card_router = CompanyCardRouter()


urlpatterns = [
    path('company/', include(company_router.get_urls())),
    path('validation-status/', include(company_validation_router.get_urls())),
    path('company-firts-item/', include(company_first_item_router.get_urls())),
    path('company-second-item/', include(company_second_item_router.get_urls())),
    path('work-day/', include(workday_router.get_urls())),
    path('employees/', include(company_employee_router.get_urls())),
    path('addresses/', include(company_address_router.get_urls())),
    path('cards/', include(company_card_router.get_urls())),
]