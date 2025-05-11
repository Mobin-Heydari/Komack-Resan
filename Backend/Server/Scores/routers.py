from django.urls import include, path
from rest_framework import routers
from .views import ServiceScoreViewSet

class ServiceScoreRouter(routers.DefaultRouter):
    """
    Custom router for ServiceScoreViewSet.

    Endpoints:
      - List:      GET /service-scores/
      - Create:    POST /service-scores/create/
      - Retrieve:  GET /service-scores/<int:pk>/
      - Update:    PUT/PATCH /service-scores/<int:pk>/update/
      - Delete:    DELETE /service-scores/<int:pk>/delete/
    """
    def __init__(self):
        super().__init__()
        # Register the viewset with an empty prefix.
        self.register(r'', ServiceScoreViewSet, basename='service_score')

    def get_urls(self):
        default_urls = super().get_urls()
        custom_urls = [
            path('', include([
                # List route: GET /service-scores/
                path('', ServiceScoreViewSet.as_view({'get': 'list'}), name='service-score-list'),
                # Create route: POST /service-scores/create/
                path('create/', ServiceScoreViewSet.as_view({'post': 'create'}), name='service-score-create'),
                # Detail routes, grouped by primary key.
                path('<int:pk>/', include([
                    # Retrieve route: GET /service-scores/<int:pk>/
                    path('', ServiceScoreViewSet.as_view({'get': 'retrieve'}), name='service-score-detail'),
                    # Update route: PUT/PATCH /service-scores/<int:pk>/update/
                    path('update/', ServiceScoreViewSet.as_view({'put': 'update', 'patch': 'update'}), name='service-score-update'),
                    # Delete route: DELETE /service-scores/<int:pk>/delete/
                    path('delete/', ServiceScoreViewSet.as_view({'delete': 'destroy'}), name='service-score-delete'),
                ])),
            ])),
        ]
        return default_urls + custom_urls
