from django.contrib import admin
from .models import Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "commune",
        "actif",
        "created_at",
    )

    list_filter = (
        "commune",
        "actif",
    )

    search_fields = (
        "nom",
        "commune",
    )