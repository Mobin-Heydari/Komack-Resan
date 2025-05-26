from django.urls import path, include

from rest_framework import routers
from . import views





class FirstItemRouter(routers.DefaultRouter):
    """
    Custom router for FirstItemViewSet.
    
    Endpoints under the base URL:
      - List:           GET /firstitems/
      - Create:         POST /firstitems/create/
      - Retrieve:       GET /firstitems/<slug:slug>/
      - Update:         PUT/PATCH /firstitems/<slug:slug>/
      - Delete:         DELETE /firstitems/<slug:slug>/
    """
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix.
        self.register(r'', views.FirstItemViewSet, basename='firstitem')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route: GET /firstitems/
                path('', views.FirstItemViewSet.as_view({'get': 'list'}), name='firstitem-list'),
                # Create route: POST /firstitems/create/
                path('create/', views.FirstItemViewSet.as_view({'post': 'create'}), name='firstitem-create'),
                # Detail routes: Retrieve, Update (PUT/PATCH), and Delete using the item slug.
                path('<slug:slug>/', include([
                    path('', views.FirstItemViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'patch': 'update',
                        'delete': 'destroy'
                    }), name='firstitem-detail'),
                ])),
            ])),
        ]
        return default_urls + custom_urls



class SecondItemRouter(routers.DefaultRouter):
    """
    Custom router for SecondItemViewSet.
    
    Endpoints under the base URL:
      - List:           GET /seconditems/
      - Create:         POST /seconditems/create/
      - Retrieve:       GET /seconditems/<slug:slug>/
      - Update:         PUT/PATCH /seconditems/<slug:slug>/
      - Delete:         DELETE /seconditems/<slug:slug>/
    """
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix.
        self.register(r'', views.SecondItemViewSet, basename='seconditem')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route: GET /seconditems/
                path('', views.SecondItemViewSet.as_view({'get': 'list'}), name='seconditem-list'),
                # Create route: POST /seconditems/create/
                path('create/', views.SecondItemViewSet.as_view({'post': 'create'}), name='seconditem-create'),
                # Detail routes: Retrieve, update and delete using the item slug.
                path('<slug:slug>/', include([
                    path('', views.SecondItemViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'patch': 'update',
                        'delete': 'destroy'
                    }), name='seconditem-detail'),
                ])),
            ])),
        ]
        return default_urls + custom_urls