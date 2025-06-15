from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuario/', include('account.urls')),
    path('eventos/', include('event.urls')),
    path('', include('core.urls')),
]