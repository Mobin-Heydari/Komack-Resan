from rest_framework import routers
from django.urls import path, include
from .views import (
    ServiceProviderProfileViewSet,
    ServiceRecipientProfileViewSet,
    AdminProfileViewSet,
    SupportProfileViewSet,
    OwnerProfileViewSet,
)


class ServiceProviderRouter(routers.DefaultRouter):
    
    def __init__(self):
        super().__init__()
        self.register(r'', ServiceProviderProfileViewSet, basename='service-provider')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', ServiceProviderProfileViewSet.as_view({'get': 'list'})),
                path('<str:user__username>/', include([
                    path('', ServiceProviderProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
                ])),
            ])),
        ]
        return urls + custom_urls


class ServiceRecipientRouter(routers.DefaultRouter):
    
    def __init__(self):
        super().__init__()
        self.register(r'', ServiceRecipientProfileViewSet, basename='service-recipient')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', ServiceRecipientProfileViewSet.as_view({'get': 'list'})),
                path('<str:user__username>/', include([
                    path('', ServiceRecipientProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
                ])),
            ])),
        ]
        return urls + custom_urls


class AdminRouter(routers.DefaultRouter):
    
    def __init__(self):
        super().__init__()
        self.register(r'', AdminProfileViewSet, basename='service-admin')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', AdminProfileViewSet.as_view({'get': 'list'})),
                path('<str:user__username>/', include([
                    path('', AdminProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
                ])),
            ])),
        ]
        return urls + custom_urls


class SupportRouter(routers.DefaultRouter):
    
    def __init__(self):
        super().__init__()
        self.register(r'', SupportProfileViewSet, basename='service-support')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', SupportProfileViewSet.as_view({'get': 'list'})),
                path('<str:user__username>/', include([
                    path('', SupportProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
                ])),
            ])),
        ]
        return urls + custom_urls
    


class OwnerRouter(routers.DefaultRouter):
    
    def __init__(self):
        super().__init__()
        self.register(r'', OwnerProfileViewSet, basename='service-support')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                path('', OwnerProfileViewSet.as_view({'get': 'list'})),
                path('<str:user__username>/', include([
                    path('', OwnerProfileViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
                ])),
            ])),
        ]
        return urls + custom_urls
