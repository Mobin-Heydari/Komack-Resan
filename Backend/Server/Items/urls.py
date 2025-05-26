from django.urls import path, include
from .routers import FirstItemRouter, SecondItemRouter



app_name = "Items"

first_item_router = FirstItemRouter()
second_item_router = SecondItemRouter()


urlpatterns = [
    path('first-item/', include(first_item_router.get_urls())),
    path('second-item/', include(second_item_router.get_urls())),
]