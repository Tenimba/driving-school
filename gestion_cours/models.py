from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User, Group
from .managers import UserManager
from django.contrib.auth.models import BaseUserManager


class UserManagers(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a new superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User_profil(AbstractUser):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    numero = models.CharField(max_length=20, null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='auth_group',
        related_query_name='auth_group',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='auth_group',
        related_query_name='auth_group',
    )
    Eleves = models.BooleanField(default=False, null=True)
    Inspecteurs = models.BooleanField(default=False, null=True)
    Secretaires = models.BooleanField(default=False, null=True)
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    objects = UserManager()

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

class Inspecteur(models.Model):
    user = models.OneToOneField(User_profil, on_delete=models.CASCADE, related_name='inspecteur')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    heuredispo = models.IntegerField(null=True, blank=True)
    heureindispo = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} {self.email} {self.user}"
    
    class Meta:
        verbose_name = 'Inspecteur'
        verbose_name_plural = 'Inspecteurs'

class Eleve(models.Model):
    user = models.OneToOneField(User_profil, on_delete=models.CASCADE, related_name='eleve')
    inspecteur = models.ForeignKey(Inspecteur, on_delete=models.CASCADE, related_name='eleve')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    heuredispo = models.IntegerField(null=True, blank=True)
    heureindispo = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} {self.email} - {self.inspecteur}"
    
    class Meta:
        verbose_name = 'Elève'
        verbose_name_plural = 'Elèves'

class Heure(models.Model):
    heurePaye = models.IntegerField()
    heureRestant = models.IntegerField(null=True, blank=True)
    user = models.OneToOneField(Eleve, on_delete=models.CASCADE, related_name='heure')

    def __str__(self):
        return f"{self.heurePaye} - {self.heureRestant} - {self.user}"
    
    class Meta:
        verbose_name = 'Heure'
        verbose_name_plural = 'Heures'

class Cours(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    inspecteur = models.ForeignKey(Inspecteur, on_delete=models.CASCADE)
    heuredebut = models.DateTimeField()
    heurefin = models.DateTimeField()
    lieu = models.CharField(max_length=100, default='25 rue de la paix 75000 Paris')
    title = models.CharField(max_length=100, default='Cours de conduite')

    def __str__(self):
        return f"{self.eleve} - {self.inspecteur} - {self.heuredebut} - {self.heurefin}"
    
    class Meta:
        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'

class Secretaire(models.Model):
    user = models.OneToOneField(User_profil, on_delete=models.CASCADE, related_name='secretaire')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nom} {self.prenom} {self.email} {self.user}"
    
    class Meta:
        verbose_name = 'Secrétaire'
        verbose_name_plural = 'Secrétaires'

class RendezVous(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='rendezvous')
    inspecteur = models.ForeignKey(Inspecteur, on_delete=models.CASCADE, related_name='rendezvous')
    heuredebut = models.TimeField()
    heurefin = models.TimeField()

    def __str__(self):
        return f"{self.eleve} - {self.inspecteur} - {self.heuredebut} - {self.heurefin}"
    
    class Meta:
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'
