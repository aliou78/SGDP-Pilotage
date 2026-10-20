from django.contrib import admin
from .models import Debarquement


@admin.register(Debarquement)
class DebarquementAdmin(admin.ModelAdmin):

    list_display = (
        'date',
        'site',
        'espece',
        'quantite',
        'archive',
        'archive_le',
        'archive_par',
    )

    actions = None

    list_filter = (
        'date',
        'site',
        'espece',
    )

    search_fields = (
        'site__nom',
        'espece__nom',
        'observation',
    )

    ordering = (
        '-date',
    )

    def has_delete_permission(self, request, obj=None):
        return False