from django.db import models

class Site(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    commune = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    actif = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nom']
        verbose_name = "Site"
        verbose_name_plural = "Sites"

    def __str__(self):
        return self.nom