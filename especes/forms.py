from django import forms
from .models import Espece


class EspeceForm(forms.ModelForm):

    class Meta:
        model = Espece

        fields = [
    'nom',
    'nom_scientifique',
    'categorie',
]
    

        labels = {
            'nom': 'Nom de l’espèce',
            'nom_scientifique': 'Nom scientifique',
            'categorie': 'Catégorie',
            'actif': 'Espèce active',
        }

        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Exemple : Sardinelle'
            }),

            'nom_scientifique': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom scientifique'
            }),

            'categorie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Exemple : Poisson pélagique'
            }),

            'actif': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }