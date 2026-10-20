from django.db import models
from django.contrib.auth import get_user_model
from sites.models import Site
from especes.models import Espece

User = get_user_model()


class Debarquement(models.Model):

    STATUT_CHOICES = (
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
    )

    date = models.DateField()

    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name='debarquements'
    )

    espece = models.ForeignKey(
        Espece,
        on_delete=models.PROTECT,
        related_name='debarquements'
    )

    quantite = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    valide_le = models.DateTimeField(null=True, blank=True)

    valide_par = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='debarquements_valides',
        null=True,
        blank=True
    )

    observation = models.TextField(
        blank=True
    )
    
    agent = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='debarquements',
        limit_choices_to={'role': 'agent'},
        null=True,
        blank=True
    )

    archive = models.BooleanField(default=False)

    archive_le = models.DateTimeField(null=True, blank=True)

    archive_par = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='debarquements_archives',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-date']
        verbose_name = "Débarquement"
        verbose_name_plural = "Débarquements"

    def __str__(self):
        return f"{self.date} - {self.site} - {self.espece}"