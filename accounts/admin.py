from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuration personnalisée du User dans l'admin Django"""
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations Supplémentaires', {
            'fields': ('role', 'telephone', 'adresse', 'actif')
        }),
    )
    
    list_display = ('username', 'get_full_name', 'email', 'get_role_display', 'actif')
    list_filter = ('role', 'actif', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Rôle et Statut', {
            'fields': ('role', 'actif')
        }),
    )
