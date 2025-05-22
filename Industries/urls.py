from django.urls import path, include
from .routers import IndustryCategoryRouter, IndustryRouter


app_name = "Industries"



urlpatterns = [
    path('industry-categories/', include(IndustryCategoryRouter().get_urls())),
    path('industries/', include(IndustryRouter().get_urls())),
]
