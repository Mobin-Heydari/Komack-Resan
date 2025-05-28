from rest_framework import routers
from django.urls import path, include

from .views import UserViewSet




class UserRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.register(r'', UserViewSet, basename='users')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', UserViewSet.as_view({'get': 'list'})),
                path('<str:username>/', include([
                    path('', UserViewSet.as_view({'get': 'retrieve'})),
                ])),
            ])),
        ]
        return urls + custom_urls