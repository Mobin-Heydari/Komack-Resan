from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('Authentication.urls', namespace='Authentication')),
    path('users/', include('Users.urls', namespace='Users')),
    path('profiles/', include('Profiles.urls', namespace='Profiles')),
    path('industries/', include('Industries.urls', namespace='Industries')),
    path('companies/', include('Companies.urls', namespace='Companies')),
    path('services/', include('Services.urls', namespace='Services')),
    path('invoices/', include('Invoices.urls', namespace='Invoices')),
]
