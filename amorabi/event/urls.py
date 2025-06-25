from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('novo/', views.evento_create, name='evento_create'),
    path('detalhe/<uuid:uuid>/', views.evento_detail, name='evento_detail'),
    path('participar/<uuid:uuid>/', views.participar_evento, name='participar_evento'),
    path('desinscrever/<uuid:uuid>/', views.desinscrever_evento, name='desinscrever_evento'),
]