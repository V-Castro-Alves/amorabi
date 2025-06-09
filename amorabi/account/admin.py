from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

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

admin.site.register(CustomUser, CustomUserAdmin)