from django.urls import path, include
from .routers import AddressRouter


app_name = "Addresses"


address_router = AddressRouter()


urlpatterns = [

]

urlpatterns = address_router.urls