from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StatusUsuario

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informações adicionais', {
            'fields': ('cpf', 'telefone', 'role'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações adicionais', {
            'fields': ('cpf', 'telefone', 'role'),
        }),
    )
    list_display = UserAdmin.list_display + ('cpf', 'telefone', 'role')

@admin.register(StatusUsuario)
class AprovacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_aprovacao', 'status', 'responsavel')
    list_filter = ('status', 'data_aprovacao')
    search_fields = ('usuario__username', 'responsavel__username')
    ordering = ('-data_aprovacao',)