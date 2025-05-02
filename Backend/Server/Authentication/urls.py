from django.urls import path
from . import views



app_name = "Authentication"



urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name="login"),
]