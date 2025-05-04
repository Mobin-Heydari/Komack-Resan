from rest_framework import routers
from django.urls import path, include
from .views import IndustryCategoryViewSet, IndustryViewSet

class IndustryCategoryRouter(routers.DefaultRouter):
    """
    Custom router for IndustryCategoryViewSet.
    URL pattern expects a slug for retrieve, update, and destroy.
    """
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix; basename is used for reverse lookups.
        self.register(r'', IndustryCategoryViewSet, basename='industry-category')

    def get_urls(self):
        # Get any default URLs from DefaultRouter.
        urls = super().get_urls()
        # Define our custom URLs.
        custom_urls = [
            path('', include([
                # List route: GET /industry-categories/
                path('', IndustryCategoryViewSet.as_view({'get': 'list'})),
                # Detail routes: GET, PUT, DELETE using the slug.
                path('<str:slug>/', include([
                    path('', IndustryCategoryViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                ])),
            ])),
        ]
        return urls + custom_urls


class IndustryRouter(routers.DefaultRouter):
    """
    Custom router for IndustryViewSet.
    The create route requires a category_slug in the URL.
    The update route supports an optional category_slug.
    """
    def __init__(self):
        super().__init__()
        self.register(r'', IndustryViewSet, basename='industry')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route: GET /industries/
                path('', IndustryViewSet.as_view({'get': 'list'})),
                # Create route: POST /industries/create/<str:category_slug>/
                path('create/<str:category_slug>/', IndustryViewSet.as_view({'post': 'create'})),
                # Retrieve, update, and destroy using the industry slug.
                path('<str:slug>/', include([
                    # Basic detail route: GET, PUT (without category_slug in URL), DELETE.
                    path('', IndustryViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'delete': 'destroy'
                    })),
                    # If a new category is provided during update: PUT /industries/<str:slug>/<str:category_slug>/
                    path('<str:category_slug>/', IndustryViewSet.as_view({
                        'put': 'update'
                    })),
                ])),
            ])),
        ]
        return urls + custom_urls
