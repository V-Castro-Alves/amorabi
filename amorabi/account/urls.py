from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='account:login'), name='logout'),
    path('cadastro/', views.cadastrar, name='cadastrar'),
    path('aprovacoes/', views.aprovacoes, name='aprovacoes'),
    path('aprovacao/<uuid:user_uuid>/', views.aprovar_usuario, name='aprovar_usuario'),
    path('resetar-senha/', views.resetar_senha, name='resetar_senha'),
]