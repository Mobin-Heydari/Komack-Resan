from django.urls import include, path
from rest_framework import routers
from .views import ProvinceViewSet, CityViewSet, RecipientAddressViewSet

class AddressRouter(routers.DefaultRouter):
    """
    Custom router for the Addresses app.

    Endpoints:
      * Province:
          - List:      GET          /provinces/
          - Create:    POST         /provinces/create/
          - Retrieve:  GET          /provinces/<slug>/
          - Update:    PUT/PATCH    /provinces/<slug>/update/
          - Delete:    DELETE       /provinces/<slug>/delete/
      
      * City:
          - List:      GET          /cities/
          - Create:    POST         /cities/create/
          - Retrieve:  GET          /cities/<slug>/
          - Update:    PUT/PATCH    /cities/<slug>/update/
          - Delete:    DELETE       /cities/<slug>/delete/

      * RecipientAddress:
          - List:      GET          /recipient-addresses/
          - Create:    POST         /recipient-addresses/create/
          - Retrieve:  GET          /recipient-addresses/<int:pk>/
          - Update:    PUT/PATCH    /recipient-addresses/<int:pk>/update/
          - Delete:    DELETE       /recipient-addresses/<int:pk>/delete/
    """
    def __init__(self):
        super().__init__()
        # Register the base viewsets to generate default list endpoints.
        self.register(r'provinces', ProvinceViewSet, basename='province')
        self.register(r'cities', CityViewSet, basename='city')
        self.register(r'recipient-addresses', RecipientAddressViewSet, basename='recipient_address')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            # Province endpoints using slug for lookup.
            path('provinces/create/', ProvinceViewSet.as_view({'post': 'create'}), name='province-create'),
            path('provinces/<slug:slug>/', ProvinceViewSet.as_view({'get': 'retrieve'}), name='province-detail'),
            path('provinces/<slug:slug>/update/', ProvinceViewSet.as_view({'put': 'update', 'patch': 'update'}), name='province-update'),
            path('provinces/<slug:slug>/delete/', ProvinceViewSet.as_view({'delete': 'destroy'}), name='province-destroy'),

            # City endpoints using slug for lookup.
            path('cities/create/', CityViewSet.as_view({'post': 'create'}), name='city-create'),
            path('cities/<slug:slug>/', CityViewSet.as_view({'get': 'retrieve'}), name='city-detail'),
            path('cities/<slug:slug>/update/', CityViewSet.as_view({'put': 'update', 'patch': 'update'}), name='city-update'),
            path('cities/<slug:slug>/delete/', CityViewSet.as_view({'delete': 'destroy'}), name='city-destroy'),

            # RecipientAddress endpoints using pk for lookup.
            path('recipient-addresses/create/', RecipientAddressViewSet.as_view({'post': 'create'}), name='recipient_address-create'),
            path('recipient-addresses/<int:pk>/', RecipientAddressViewSet.as_view({'get': 'retrieve'}), name='recipient_address-detail'),
            path('recipient-addresses/<int:pk>/update/', RecipientAddressViewSet.as_view({'put': 'update', 'patch': 'update'}), name='recipient_address-update'),
            path('recipient-addresses/<int:pk>/delete/', RecipientAddressViewSet.as_view({'delete': 'destroy'}), name='recipient_address-destroy'),
        ]
        # Concatenate the default URLs (like list endpoints) with our custom URLs.
        return default_urls + custom_urls
