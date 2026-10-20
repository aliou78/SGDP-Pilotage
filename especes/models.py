from django.db import models


class Espece(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    nom_scientifique = models.CharField(max_length=150, blank=True)
    categorie = models.CharField(max_length=100, blank=True)
    actif = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "Espèce"
        verbose_name_plural = "Espèces"

    def __str__(self):
        return self.nom