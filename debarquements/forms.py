from django import forms
from .models import Debarquement
from sites.models import Site
from especes.models import Espece


class DebarquementForm(forms.ModelForm):

    class Meta:
        model = Debarquement

        fields = [
            'date',
            'site',
            'espece',
            'quantite',
            'observation',
        ]

        labels = {
            'date': 'Date',
            'site': 'Site',
            'espece': 'Espèce',
            'quantite': 'Quantité (kg)',
            'observation': 'Observation',
        }

        widgets = {
            'date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),

            'site': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'espece': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'quantite': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Exemple : 150.50',
                    'step': '0.01',
                    'min': '0',
                }
            ),

            'observation': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Observation éventuelle...',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['site'].queryset = Site.objects.filter(
            actif=True
        )

        self.fields['espece'].queryset = Espece.objects.filter(
            actif=True
        )