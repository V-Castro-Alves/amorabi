from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuario/', include('account.urls')),
    #path('dashboard/', include('dashboard.urls')),
    path('eventos/', include('event.urls')),
    #path('notificacao/', include('notification.urls')),
    #path('financeiro/', include('finance.urls')),
    path('', RedirectView.as_view(pattern_name='event:event_list', permanent=False), name='root-redirect'),
]