from django.urls import path, include
from .routers import ServiceProviderRouter, ServiceRecipientRouter, AdminRouter, SupportRouter


app_name = "Profiles"



urlpatterns = [
    path('providers/', include(ServiceProviderRouter().get_urls())),
    path('recipients/', include(ServiceRecipientRouter().get_urls())),
    path('admins/', include(AdminRouter().get_urls())),
    path('support/', include(SupportRouter().get_urls())),
]
