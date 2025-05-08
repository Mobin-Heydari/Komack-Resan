from rest_framework import routers
from django.urls import path, include

from . import views




class CompanyRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'companies', views.CompanyViewSet, basename='users')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', views.CompanyViewSet.as_view({'get': 'list'})),
                path('<slug:slug>/', include([
                    path('', views.CompanyViewSet.as_view({'get': 'retrieve'})),
                ])),
            ])),
        ]
        return urls + custom_urls