from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('Authentication.urls', namespace='Authentication')),
    path('users/', include('Users.urls', namespace='Users')),
    path('profiles/', include('Profiles.urls', namespace='Profiles')),
    path('industries/', include('Industries.urls', namespace='Industries')),
    path('companies/', include('Companies.urls', namespace='Companies')),
    path('services/', include('Services.urls', namespace='Services')),
    path('invoices/', include('Invoices.urls', namespace='Invoices')),
    path('payments/', include('Payments.urls', namespace='Payments')),
    path('addresses/', include('Addresses.urls', namespace='Addresses')),
    path('accounts/', include('Accounts.urls', namespace='Accounts')),
    path('scores/', include('Scores.urls', namespace='Scores')),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
