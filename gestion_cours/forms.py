from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import User_profil, Inspecteur, Eleve, Cours, RendezVous, Heure, Secretaire

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    username = forms.CharField(max_length=30)
    nom = forms.CharField(max_length=30)
    prenom = forms.CharField(max_length=30)
    numero = forms.CharField(max_length=30)

    ROLES_CHOICES = (
        ('inspecteur', 'Inspecteur'),
        ('eleve', 'Élève'),
        ('secretaire', 'Secrétaire')
    )
    role = forms.ChoiceField(choices=ROLES_CHOICES)

    class Meta:
        model = User_profil
        fields = ('username', 'email', 'role', 'nom', 'prenom', 'numero')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ConnexionFrom(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User_profil
        fields = ('username', 'password')

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nom = forms.CharField(max_length=30)
    prenom = forms.CharField(max_length=30)
    numero = forms.CharField(max_length=30)

    ROLES_CHOICES = (
        ('inspecteur', 'Inspecteur'),
        ('eleve', 'Élève'),
        ('secretaire', 'Secrétaire')
    )
    role = forms.ChoiceField(choices=ROLES_CHOICES)

    class Meta:
        model = User_profil
        fields = ('username', 'email', 'nom', 'prenom', 'numero', 'password1', 'password2', 'role')


class RDVForm(forms.ModelForm):
    eleve = forms.ModelChoiceField(queryset=Eleve.objects.all(), label='Élève')
    date = forms.DateField(widget=forms.SelectDateWidget, label='Date')
    heuredebut = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), label='Heure de début')


    class Meta:
        model = RendezVous
        fields = ['eleve', 'date', 'heuredebut', 'heurefin']


class InspecteurForm(forms.ModelForm):
    numero = forms.CharField(max_length=30)
    class Meta:
        model = Inspecteur
        fields = ('nom', 'prenom', 'email')

class EleveForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ('email', 'nom', 'prenom', 'inspecteur')
    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.email} - {self.inspecteur})"

class SecretaireForm(forms.ModelForm):
    numero = forms.CharField(max_length=30)
    class Meta:
        model = Secretaire
        fields = ('nom', 'prenom', 'email')

class CoursForm(forms.ModelForm):
    title = forms.CharField(max_length=30, label='Titre', widget=forms.TextInput(attrs={'class': 'cours_title'}))
    lieux = forms.CharField(max_length=30, label='Lieux', widget=forms.TextInput(attrs={'class': 'cours_lieux'}))
    eleve = forms.ModelChoiceField(queryset=Eleve.objects.all(), label='Élève', widget=forms.Select(attrs={'class': 'cours_eleve'}))
    inspcteur = forms.ModelChoiceField(queryset=Inspecteur.objects.all(), label='Inspecteur', widget=forms.Select(attrs={'class': 'cours_inspecteur'}))
    heuredebut = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local', 'class': 'cours_heuredebut'}), label='Heure de début')
    une_heure = forms.BooleanField(required=False, label="1 heure", widget=forms.CheckboxInput(attrs={'class': 'cours_une_heure'}))
    deux_heures = forms.BooleanField(required=False, label="2 heures", widget=forms.CheckboxInput(attrs={'class': 'cours_deux_heures'}))
    trois_heures = forms.BooleanField(required=False, label="3 heures", widget=forms.CheckboxInput(attrs={'class': 'cours_trois_heures'}))

    class Meta:
        model = Cours
        fields = ('title','lieux','eleve', 'inspcteur', 'heuredebut')

    def __init__(self, *args, **kwargs):
      user = kwargs.pop('user', None)
      super().__init__(*args, **kwargs)
      if user is not None:
          if Inspecteur.objects.filter(email=user.email).exists():
              inspecteur = Inspecteur.objects.get(email=user.email)
              self.fields['eleve'].queryset = Eleve.objects.filter(inspecteur=inspecteur)
              self.fields['inspcteur'].queryset = Inspecteur.objects.filter(email=user.email)
              self.fields['inspcteur'] = forms.CharField(initial=inspecteur, disabled=True)
          elif user.is_superuser or Secretaire.objects.filter(email=user.email).exists():
              self.fields['eleve'].queryset = Eleve.objects.all()
              self.fields['inspcteur'].queryset = Inspecteur.objects.all()
      else :
          print('user est none') 
          

    def clean(self):
        cleaned_data = super().clean()
        heuredebut = cleaned_data.get('heuredebut')
        if heuredebut:
            heurefin = heuredebut
            if cleaned_data.get('une_heure'):
                heurefin += timedelta(hours=1)
            if cleaned_data.get('deux_heures'):
                heurefin += timedelta(hours=2)
            if cleaned_data.get('trois_heures'):
                heurefin += timedelta(hours=3)
            cleaned_data['heurefin'] = heurefin
        return cleaned_data

class CoursUpdateForm(forms.ModelForm):
    title = forms.CharField(max_length=30, label='Titre', widget=forms.TextInput(attrs={'class': 'cours_title'}))
    lieux = forms.CharField(max_length=30, label='Lieux', widget=forms.TextInput(attrs={'class': 'cours_lieux'}))
    heuredebut = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local', 'class': 'cours_heuredebut', 'readonly': True}), label='Heure de début')
    heurefin = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local', 'class': 'cours_heurefin', 'readonly': True}), label='Heure de fin')
    
    
    class Meta:
        model = Cours
        fields = ('title','lieux','heuredebut')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['heuredebut'].widget.attrs['value'] = instance.heuredebut.strftime('%Y-%m-%dT%H:%M')
            self.fields['heuredebut'].widget.attrs['readonly'] = True
            self.fields['heuredebut'].label = 'Heure de début (Non modifiable)'
            self.fields['heurefin'].widget.attrs['value'] = instance.heurefin.strftime('%Y-%m-%dT%H:%M')
            self.fields['heurefin'].widget.attrs['readonly'] = True
            self.fields['heurefin'].label = 'Heure de fin (Non modifiable)'



class HeurePayeForm(forms.ModelForm):
    heure = forms.IntegerField(label='Heure')
    user = forms.ModelChoiceField(queryset=Eleve.objects.all(), label='Élève')
    prix_horaire = forms.DecimalField(label='Prix horaire', initial=35, disabled=True)

    class Meta:
        model = Heure
        fields = ['user','heure', 'prix_horaire']

class AjoutHeurePayeeForm(forms.ModelForm):
    heure_payee = forms.IntegerField()
    user = forms.ModelChoiceField(queryset=Eleve.objects.all(), label='Élève')

    class Meta:
        model = Heure
        fields = ('user', 'heure_payee')

    def clean(self):
        cleaned_data = super().clean()
        heure_payee = cleaned_data.get("heure_payee")
        user = cleaned_data.get("user")
        # Vérifier que les champs heure_payee et prix_horaire sont valides
        if heure_payee is None or heure_payee <= 0:
            raise forms.ValidationError("Le nombre d'heures payées doit être supérieur à 0")
        # Vérifier si l'instance Heure pour cet Eleve existe déjà
        try:
            heure = Heure.objects.get(user=user)
            heure.heurePaye += heure_payee  # Ajouter les heures payées existantes
            heure.save()
            raise forms.ValidationError("Les heures payées ont été mises à jour.")
        except Heure.DoesNotExist:
            pass

        return cleaned_data

class HeureDispoForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['heuredispo', 'heureindispo']
        labels = {
            'heuredispo': 'Début de disponibilité',
            'heureindispo': 'Fin de disponibilité'
        }
        widgets = {
            'debut de disponibilite': forms.TextInput( attrs={'placeholder': 'ex: 8'}),
            'fin de disponibilite': forms.TextInput( attrs={'placeholder': 'ex: 19'})
        }

class HeureDispoFormInspecteur(forms.ModelForm):
    class Meta:
        model = Inspecteur
        fields = ['heuredispo', 'heureindispo']
        labels = {
            'heuredispo': 'Début de disponibilité',
            'heureindispo': 'Fin de disponibilité'
        }
        widgets = {
            'heuredispo': forms.TextInput(attrs={'placeholder': 'ex: 8'}),
            'heureindispo': forms.TextInput(attrs={'placeholder': 'ex: 15'})
        }

