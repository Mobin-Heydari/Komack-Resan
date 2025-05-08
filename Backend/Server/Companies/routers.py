from django.urls import include, path
from rest_framework import routers
from . import views




class CompanyRouter(routers.DefaultRouter):
    """
    Custom router for CompanyViewSet.
    
    Endpoints under /companies/:
      - List:           GET /companies/
      - Create:         POST /companies/create/
      - Retrieve:       GET /companies/<slug:slug>/
      - Update:         PUT/PATCH /companies/<slug:slug>/
      - Delete:         DELETE /companies/<slug:slug>/
      
    You can easily extend the update route to support additional URL parameters if needed.
    """
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix so that our custom URLs under /companies/ work.
        self.register(r'company', views.CompanyViewSet, basename='company')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route: GET /companies/
                path('', views.CompanyViewSet.as_view({'get': 'list'})),
                # Create route: POST /companies/create/
                path('create/', views.CompanyViewSet.as_view({'post': 'create'})),
                # Retrieve, update, and delete using the company slug.
                path('<slug:slug>/', include([
                    # Basic detail route: GET, PUT/PATCH, DELETE.
                    path('', views.CompanyViewSet.as_view({
                        'get': 'retrieve',
                        'put': 'update',
                        'patch': 'update',
                        'delete': 'destroy'
                    })),
                    # Optionally, if ever you need a route with an extra parameter for update
                    # path('<str:extra>/', views.CompanyViewSet.as_view({'put': 'update'})),
                ])),
            ])),
        ]
        return urls + custom_urls

