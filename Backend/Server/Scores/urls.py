from django.urls import path, include
from .routers import ServiceScoreRouter




app_name = "Scores"


service_score_router = ServiceScoreRouter()


urlpatterns = [
    path('services/', include(service_score_router.get_urls())),
]