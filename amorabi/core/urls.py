from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('o-itinga/', views.o_itinga, name='o_itinga'),
    path('sobre-nos/', views.sobre_nos, name='sobre_nos'),
]