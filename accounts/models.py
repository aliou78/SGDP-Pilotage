from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Modèle User personnalisé avec rôles"""
    
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('chef', 'Chef de Service'),
        ('agent', 'Agent de Collecte'),
        ('consultation', 'Consultation'),
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='agent'
    )
    
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    actif = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['username']
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        self.is_active = self.actif
        super().save(*args, **kwargs)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_chef(self):
        return self.role == 'chef'
    
    def is_agent(self):
        return self.role == 'agent'

    def is_consultation(self):
        return self.role == 'consultation'
