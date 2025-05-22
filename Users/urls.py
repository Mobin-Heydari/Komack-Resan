from django.urls import path, include
from .routers import UserRouter, IdCardRouter



app_name = "Users"


user_router = UserRouter()
id_card_router = IdCardRouter()


urlpatterns = [
    path('user/', include(user_router.get_urls())),
    path('id-card/', include(id_card_router.get_urls())),
]