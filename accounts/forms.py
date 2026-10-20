from django import forms
from .models import User


class UserCreateForm(forms.ModelForm):

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Mot de passe'
            }
        )
    )

    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            'role',
            'telephone',
            'adresse',
            'actif',
        ]

        labels = {
            'username': "Nom d'utilisateur",
            'first_name': "Prénom",
            'last_name': "Nom",
            'password': "Mot de passe",
            'role': "Rôle",
            'telephone': "Téléphone",
            'adresse': "Adresse",
            'actif': "Compte actif",
        }

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'role': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'telephone': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'adresse': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),

            'actif': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)

        # Important : le mot de passe doit être haché
        user.set_password(
            self.cleaned_data['password']
        )

        if commit:
            user.save()

        return user


class UserUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        self._existing_password = instance.password if instance else None
        super().__init__(*args, **kwargs)

    password = forms.CharField(
        label="Nouveau mot de passe",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Laisser vide pour conserver le mot de passe'
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            'role',
            'telephone',
            'adresse',
            'actif',
        ]
        widgets = UserCreateForm.Meta.widgets
        labels = UserCreateForm.Meta.labels

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        else:
            user.password = self._existing_password
        if commit:
            user.save()
        return user