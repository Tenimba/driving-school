import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.utils import timezone
from rest_framework import viewsets, status
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Inspecteur, Eleve, Cours, Secretaire, RendezVous, User_profil, Heure
from .forms import InspecteurForm, EleveForm, CoursForm, HeurePayeForm, AjoutHeurePayeeForm
from .forms import InscriptionForm, RDVForm, ConnexionFrom,CoursUpdateForm, HeureDispoForm, HeureDispoFormInspecteur, SecretaireForm

from django.db import transaction
from .managers import UserManager
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from .forms import SignUpForm, ConnexionFrom
from django.http import JsonResponse
import random
import datetime
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from .serializers import InspecteurSerializer, EleveSerializer, CoursSerializer, SecretaireSerializer

logger = logging.getLogger(__name__)

class InspecteurViewSet(viewsets.ModelViewSet):
    serializer_class = InspecteurSerializer
    queryset = Inspecteur.objects.all()

def ispecteur_list(request):
    if request.method == 'GET':
        inspecteurs = Inspecteur.objects.all()
        serializer = InspecteurSerializer(inspecteurs, many=True)
        return JsonResponse(serializer.data, safe=False)

class EleveViewSet(viewsets.ModelViewSet):
    serializer_class = EleveSerializer
    queryset = Eleve.objects.all()

@login_required
def eleve_list(request):
    utilisateur = User_profil.objects.get(email=request.user.email)
    if request.method == 'GET':
        if request.user.is_superuser:
            eleves = Eleve.objects.all()
            inspecteurs = Inspecteur.objects.all()
            Secretaires = Secretaire.objects.all()
            serializer = EleveSerializer(eleves, many=True)
            return render(request, 'auto_ecole/eleve.html', {'eleves': eleves, 'inspecteurs': inspecteurs, 'secretaires': Secretaires})
        if Secretaire.objects.filter(email=utilisateur.email).exists():
            eleves = Eleve.objects.all()
            inspecteurs = Inspecteur.objects.all()
            serializer = EleveSerializer(eleves, many=True)
            return render(request, 'auto_ecole/eleve.html', {'eleves': eleves, 'inspecteurs': inspecteurs})
        elif Inspecteur.objects.filter(email=utilisateur.email).exists():
            eleves = Eleve.objects.all()
            inste = Inspecteur.objects.get(email=request.user.email)
            el = Eleve.objects.filter(inspecteur=inste)
            return render(request, 'auto_ecole/eleve.html', {'eleves': el})
        elif Eleve.objects.filter(email=utilisateur.email).exists():
            eleves = Eleve.objects.get(email=utilisateur.email)
            inspecteur = Inspecteur.objects.get(id=eleves.inspecteur.id)
            utilisateur = User_profil.objects.get(email=eleves.user.email)
            try:
              heure =  Heure.objects.get(user=eleves.id)
              heurePaye = heure.heurePaye
              heurecalcule = heure.heureRestant - heure.heurePaye
            except:
                heure =  Heure.objects.get(user=eleves.id)
                heurePaye = heure.heurePaye
                heurecalcule = 0
            else:
                heurePaye = 0
                heurecalcule = 0
            return render(request, 'auto_ecole/eleve_detail.html', {'eleve': eleves, 'heure': heurecalcule, 'utilisateur': utilisateur, 'heurePaye': heurePaye, 'inspecteur': inspecteur})
        else:
            messages.error(request, "Vous n'avez pas les droits pour accéder à cette page")
            return redirect('index')

def deconnexion(request):
    logout(request)
    return redirect('login')
            
def delete_eleve(request, id):
    if Eleve.objects.get(id=id):
        eleve = Eleve.objects.get(id=id)
        heure= Heure.objects.get(user=eleve.id)
        heure.delete()
        profil = User_profil.objects.get(email=eleve.user.email)
        profil.is_active = False
        profil.delete()
        eleve.delete()
        messages.success(request, "{} a ete supprime".format(eleve.user.username))
        return redirect('eleve_list')
    elif Inspecteur.objects.get(id=id):
        inspecteur = Inspecteur.objects.get(id=id)
        profil = User_profil.objects.get(email=inspecteur.user.email)
        profil.is_active = False
        profil.delete()
        inspecteur.delete()
        messages.success(request, "l'Eleve {} a ete supprime".format(inspecteur.user.username))
        return redirect('eleve_list')
    else:
        messages.error(request, "personne a ete supprime")
        return redirect('index')

def eleve_detail(request, id):
    utilisateur = User_profil.objects.get(email=request.user.email)
    if Inspecteur.objects.filter(email=utilisateur.email).exists():
      eleve = Eleve.objects.get(id=id)
      utilisateur = User_profil.objects.get(email=eleve.user.email)
      if Heure.objects.filter(user=eleve.id).exists() :
        heure =  Heure.objects.get(user=eleve.id)
        heurePaye = heure.heurePaye
        heureRestant = heure.heureRestant or 0
        heurecalcule = heurePaye - heureRestant
      else:
          heurePaye = 0
          heurecalcule = 0
      return render(request, 'auto_ecole/eleve_detail.html', {'eleve': eleve, 'heure': heureRestant, 'utilisateur': utilisateur, 'heurePaye': heurePaye, 'heurecalcule': heurecalcule})
    elif Secretaire.objects.filter(email=utilisateur.email).exists() or request.user.is_superuser:
         eleve = Eleve.objects.get(id=id)
         inspecteur = Inspecteur.objects.get(id=eleve.inspecteur.id)
         utilisateur = User_profil.objects.get(email=eleve.user.email)
         if Heure.objects.filter(user=eleve.id).exists() :
           heure =  Heure.objects.get(user=eleve.id)
           heurePaye = heure.heurePaye
           heureRestant = heure.heureRestant or 0
           heurecalcule = heure.heurePaye - heureRestant
           if heurecalcule < 0:
               heurecalcule = 0
           elif heurecalcule == heurePaye:
                heurecalcule = 0
           else:
               heurecalcule = heurecalcule
         else:
             heurePaye = 0
             heureRestant = 0
             heurecalcule = 0
         return render(request, 'auto_ecole/eleve_detail.html', {'eleve': eleve, 'heure': heureRestant, 'utilisateur': utilisateur, 'heurePaye': heurePaye, 'inspecteur': inspecteur, 'heurecalcule': heurecalcule})
    elif Eleve.objects.filter(email=utilisateur.email).exists():
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page")
        return redirect('profile')
    else:
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page")
        return redirect('profile')

def inspecteur_detail(request, id):
    if Secretaire.objects.filter(email=request.user.email).exists() or request.user.is_superuser or Inspecteur.objects.filter(email=request.user.email).exists():
        inspecteurs = Inspecteur.objects.get(id=id)
        utilisateur = User_profil.objects.get(email=inspecteurs.email)
        return render(request, 'auto_ecole/inspecteur.html', {'inspecteur': inspecteurs, 'utilisateur': utilisateur})
    
def secretaire_detail(request, id):
    if request.user.is_superuser:
        secretaire = Secretaire.objects.get(id=id)
        print(secretaire.user)
        # utilisateur = User_profil.objects.get(email=secretaire.email)
        return render(request, 'auto_ecole/secretaire.html', {'secretaire': secretaire, 'utilisateur': secretaire.user})

def secretaire_delete(request, id):
    if Secretaire.objects.get(id=id):
        secretaire = Secretaire.objects.get(id=id)
        profil = User_profil.objects.get(email=secretaire.user.email)
        profil.is_active = False
        profil.delete()
        secretaire.delete()
        messages.success(request, "la secretaire {} a ete supprime".format(secretaire.user.username))
        return redirect('eleve_list')

def delete_inscpetur(request, id):
    if Inspecteur.objects.get(id=id):
        inspecteur = Inspecteur.objects.get(id=id)
        try:
          cours = Cours.objects.get(inspecteur=inspecteur.id)
          Eleven = Eleve.objects.get(inspecteur=inspecteur.id)
          Eleven.inspecteur = Inspecteur.objects.all().ramdom()
          Eleven.save()
          cours.delete()
          profil = User_profil.objects.get(email=inspecteur.user.email)
          profil.is_active = False
          profil.delete()
          inspecteur.delete()
          messages.success(request, "Linspecteur {} a ete supprime".format(inspecteur.user.username))
          return redirect('eleve_list')
        except:
           profil = User_profil.objects.get(email=inspecteur.user.email)
           profil.is_active = False
           profil.delete()
           inspecteur.delete()
           messages.success(request, "L'inspecteur {} a ete supprime".format(inspecteur.user.username))
           return redirect('eleve_list')
    else:
        messages.error(request, "personne a ete supprime")
        return redirect('index')

class CoursViewSet(viewsets.ModelViewSet):
    serializer_class = CoursSerializer
    queryset = Cours.objects.all()

def cours_list(request):
    if request.method == 'GET':
        cours = Cours.objects.all()
        serializer = CoursSerializer(cours, many=True)
        return JsonResponse(serializer.data, safe=False)

class SecretaireViewSet(viewsets.ModelViewSet):
    serializer_class = SecretaireSerializer
    queryset = Secretaire.objects.all()

def secretaire_list(request):
    if request.method == 'GET':
        secretaire = Secretaire.objects.all()
        serializer = SecretaireSerializer(secretaire, many=True)
        return JsonResponse(serializer.data, safe=False)

def inscription(request):
    if request.user.is_superuser:
      if request.method == 'POST':
          form = SignUpForm(request.POST)
          if form.is_valid():
              username = form.cleaned_data.get('username')
              nom = form.cleaned_data.get('nom')
              prenoom = form.cleaned_data.get('prenom')
              email = form.cleaned_data.get('email')
              password = form.cleaned_data.get('password1')
              numero = form.cleaned_data.get('numero')
              user = User_profil.objects.create(username=username, first_name=nom, last_name=prenoom, email=email, numero=numero)
              user.set_password(password)
              user.save()
              role = form.cleaned_data.get('role')
              if role == 'eleve':
                  try:
                      incritpion = Inspecteur.objects.all()
                      inspecteurs = random.choice(incritpion)
                      Eleve.objects.create(user=user, nom=form.cleaned_data.get('nom'), prenom=form.cleaned_data.get('prenom'), email=form.cleaned_data.get('email'), inspecteur=inspecteurs)
                      user_profil = User_profil.objects.get(email=email)
                      user.Eleves = True
                      user.save()
                      login(request, user=user)
                      messages.success(request, f"Compte de l'eleve {username} a ete cree ! Merci de vous connecter")
                  except Exception as e:
                      messages.error(request, f"Erreur lors de la création de l'élève: {e}")
                      return redirect('inscription')
              
              elif role == 'inspecteur':
                  try:
                      Inspecteur.objects.create(user=user, nom=form.cleaned_data.get('nom'), prenom=form.cleaned_data.get('prenom'), email=form.cleaned_data.get('email'))
                      user_profil = User_profil.objects.get(email=email)
                      user_profil.Inspecteurs = True
                      user_profil.save()
                      login(request, user=user)
                      messages.success(request, f"Compte créé pour {username}! Merci de vous connecter")
                  except Exception as e:
                      messages.error(request, f"Erreur lors de la création de l'inspecteur: {e}")
                      return redirect('inscription')
              elif role == 'secretaire':
                  try:
                      Secretaire.objects.create(user=user, nom=form.cleaned_data.get('nom'), prenom=form.cleaned_data.get('prenom'), email=form.cleaned_data.get('email'))
                      user_profil = User_profil.objects.get(email=email)
                      user_profil.Secretaires = True
                      user_profil.save()
                      login(request, user=user)
                      messages.success(request, f"Compte créé pour {username}! Merci de vous connecter")
                  except Exception as e:
                      messages.error(request, f"Erreur lors de la création de la secrétaire: {e}")
                      return redirect('inscription')
              return redirect('profile')
          else:
             messages.error(request, "Le formulaire est invalide. Veuillez corriger les erreurs ci-dessous.")
             for field, errors in form.errors.items():
                 for error in errors:
                     messages.error(request, f"{field}: {error}")
             return redirect('inscription')
  
      else:
          form = SignUpForm()
      return render(request, 'auto_ecole/inscription.html', {'form': form})
    else:
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page")
        return redirect('logins')

@login_required
def ajouterheure(request):
    utilisateur = User_profil.objects.get(email=request.user.email)
    if Secretaire.objects.filter(email=request.user.email).exists() or request.user.is_superuser:
      if request.method == 'POST':
          form = AjoutHeurePayeeForm(request.POST)
          if form.is_valid():
              eleve = form.cleaned_data.get('user')
              heure_payee = form.cleaned_data.get('heure_payee')
              try:
                  heure = Heure.objects.get(user=eleve)
                  heure.heurePaye += heure_payee
                  heure.save()
              except Heure.DoesNotExist:
                  heure = Heure(user=eleve, heurePaye=heure_payee)
                  heure.save()
  
              return redirect('profile')
          else:
               messages.success(request, f" {form.cleaned_data.get('heure_payee')} heure(s) on ete ajouter a votre compte.")
      else:
          form = AjoutHeurePayeeForm()
    else:
        messages.error(request, "Vous n'avez pas les droits pour accéder à cette page")
        return redirect('profile')

    return render(request, 'auto_ecole/heure_paye.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        form = ConnexionFrom(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user=user)
                messages.success(request, f"Vous êtes connecté en tant que {username}")
                return redirect('profile')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
        else:
            messages.error(request, "Le formulaire est invalide")
    form = ConnexionFrom()
    return render(request, 'auto_ecole/login.html', {'form': form})


def cours_list(request):
      if Eleve.objects.filter(email=request.user.email).exists():
          eleves = Eleve.objects.get(user=request.user)
          cours = Cours.objects.all()
          course = cours.filter(eleve_id=eleves.id)
          Inspecteurs = Inspecteur.objects.all()
          HeurePayee = Heure.objects.get(user=eleves.id)
          events = []
          for c in course:
              eleve = c.eleve
              heure = Heure.objects.filter(user=eleve).first()
              if heure is None:
                  print(f"No Heure object found for Eleve {eleve}")
              else:
               event = {
                  'id': c.id,
                  'user': 'eleve',
                  'title': c.title,
                  'start': c.heuredebut,
                  'end': c.heurefin,
                  'lieux': c.lieu,
                  'name': c.title,
                  'eleve': eleve.nom,
                  'heurePayee': HeurePayee.heurePaye,
                  'heureRestante': HeurePayee.heureRestant,
                  'inspecteur': heure.user.inspecteur.nom,
              }
              events.append(event)
          return JsonResponse(events, safe=False)
      elif Inspecteur.objects.filter(email=request.user.email).exists():
          Inspecteurs = Inspecteur.objects.get(user=request.user)
          cours = Cours.objects.all()
          course = cours.filter(inspecteur_id=Inspecteurs.id)
          events = []
          for c in course:
              eleve = c.eleve
              heure = Heure.objects.filter(user=eleve).first()
              if heure is None:
                  print(f"No Heure object found for Eleve {eleve}")
              else:
                  event = {
                      'id': c.id,
                      'user': 'inspecteur',
                      'title': c.title,
                      'start': c.heuredebut,
                      'end': c.heurefin,
                      'lieux': c.lieu,
                      'name': c.title,
                      'eleve': eleve.nom,
                      'heurePayee': heure.heurePaye,
                      'heureRestante': heure.heureRestant,
                      'inspecteur': Inspecteurs.nom,
                  }
            
                  events.append(event)
          return JsonResponse(events, safe=False)
      elif Secretaire.objects.filter(email=request.user.email).exists() or request.user.is_superuser:
          cours = Cours.objects.filter(inspecteur__isnull=False, eleve__isnull=False, heuredebut__isnull=False)
          events = []
          for c in cours:
              eleve = c.eleve
              if Heure.objects.filter(user=eleve).exists():
                  heure = Heure.objects.filter(user=eleve).first()
                  event = {
                      'id': c.id,
                      'user': "secretaire",
                      'title': eleve.nom,
                      'start': c.heuredebut,
                      'end': c.heurefin,
                      'lieux': c.lieu,
                      'eleve': eleve.nom,
                      'name': c.title,
                      'heurePayee': heure.heurePaye,
                      'heureRestante': heure.heureRestant,
                      'inspecteur': c.inspecteur.nom,
                  }
              else:
                  event = {
                      'id': c.id,
                      'user': "secretaire",
                      'title': eleve.nom,
                      'start': c.heuredebut,
                      'end': c.heurefin,
                      'lieux': c.lieu,
                       'name': c.title,
                       'eleve': eleve.nom,
                      'heurePayee': '0',
                      'heureRestante': '0',
                      'inspecteur': c.inspecteur.nom,
                  }
              events.append(event)
          return JsonResponse(events, safe=False)
      elif request.user.is_superuser:
          cours = Cours.objects.filter(inspecteur__isnull=False, eleve__isnull=False, heuredebut__isnull=False)
          events = []
          for c in cours:
              eleve = c.eleve
              if Heure.objects.filter(user=eleve).exists():
                  heure = Heure.objects.filter(user=eleve).first()
                  event = {
                      'id': c.id,
                      'user': "secretaire",
                      'title': eleve.nom,
                      'start': c.heuredebut,
                      'end': c.heurefin,
                      'lieux': c.lieu,
                      'eleve': eleve.nom,
                      'name': c.title,
                      'heurePayee': heure.heurePaye,
                      'heureRestante': heure.heureRestant,
                      'inspecteur': c.inspecteur.nom,
                  }
              else:
                  event = {
                      'id': c.id,
                      'user': "secretaire",
                      'title': eleve.nom,
                      'start': c.heuredebut,
                      'end': c.heurefin,
                      'lieux': c.lieu,
                       'name': c.title,
                       'eleve': eleve.nom,
                      'heurePayee': '0',
                      'heureRestante': '0',
                      'inspecteur': c.inspecteur.nom,
                  }
              events.append(event)
          return JsonResponse(events, safe=False)
      else:
          messages.error(request, "Vous n'avez pas les droits pour accéder à cette page")
          return redirect('login')
        
def profil(request):
    utilisateur = User_profil.objects.get(email=request.user.email)
    if Eleve.objects.filter(email=request.user.email).exists():
        eleve = Eleve.objects.get(user=utilisateur.id)
        cours = Cours.objects.all()
        course = cours.filter(eleve_id=eleve.id)
        Inspecteurs = Inspecteur.objects.all()
        # HeurePayee = Heure.objects.get(user=eleve.id)
        heure = Heure.objects.all()
        HeurePayee = heure.filter(user=eleve)
        events = []
        for c in course:
            eleve = c.eleve
            heure = Heure.objects.filter(user=eleve).first()
            if heure is None or heure.heureRestant is None:
                event = {
                'id': c.id,
                'user': "eleve",
                'title': c.title,
                'start': c.heuredebut.strftime("%Y-%m-%d %H:%M:%S"),
                'end': c.heurefin.strftime("%Y-%m-%d %H:%M:%S"),
                'lieux': c.lieu,
                'name': c.title,
                'eleve': eleve.nom,
                'dispodebut': eleve.heuredispo,
                'dispofin': eleve.heureindispo,
                'heurePayee': heure.heurePaye,
                'heureRestante': 0,
                'inspecteur': heure.user.inspecteur.nom,
            }
            else:
             event = {
                'id': c.id,
                'user': "eleve",
                'title': c.title,
                'start': c.heuredebut.strftime("%Y-%m-%d %H:%M:%S"),
                'end': c.heurefin.strftime("%Y-%m-%d %H:%M:%S"),
                'lieux': c.lieu,
                'name': c.title,
                'eleve': eleve.nom,
                'dispodebut': eleve.heuredispo,
                'dispofin': eleve.heureindispo,
                'heuresPayee': heure.heurePaye,
                'heuresRestante': heure.heureRestant,
                'inspecteur': heure.user.inspecteur.nom,
            }
            events.append(event)
        JsonResponse(events, safe=False)
        context = {'events': events, 'timenow': timezone.now()}
        return render(request, 'auto_ecole/profil.html', context)
    elif Inspecteur.objects.filter(email=request.user.email).exists():
        Inspecteurs = Inspecteur.objects.get(email=request.user.email)
        cours = Cours.objects.all()
        course = cours.filter(inspecteur_id=Inspecteurs.id)
        events = []
        for c in course:
            eleve = c.eleve
            heure = Heure.objects.filter(user=eleve).first()
            if heure is None:
                print(f"No Heure object found for Eleve {eleve}")
            else:
                event = {
                    'id': c.id,
                    'user': "inspecteur",
                    'title': heure.user.nom,
                    'start': c.heuredebut.strftime("%Y-%m-%d %H:%M:%S"),
                    'end': c.heurefin.strftime("%Y-%m-%d %H:%M:%S"),
                    'lieux': c.lieu,
                    'name': c.title,
                    'eleve': eleve.nom,
                    'heurePayee': heure.heurePaye,
                    'heureRestante': heure.heureRestant,
                    'inspecteur': Inspecteurs.nom,
                }
                events.append(event)
        JsonResponse(events, safe=False)
        context = {'events': events, 'timenow': timezone.now()}
        return render(request, 'auto_ecole/profil.html', context)
    elif Secretaire.objects.filter(email=request.user.email).exists() or request.user.is_superuser:
        cours = Cours.objects.filter(inspecteur__isnull=False, eleve__isnull=False, heuredebut__isnull=False)
        events = []
        for c in cours:
            eleve = c.eleve
            if Heure.objects.filter(user=eleve).exists():
                heure = Heure.objects.filter(user=eleve).first()
                event = {
                    'id': c.id,
                    'user': "secretaire",
                    'title': eleve.nom,
                    'start': c.heuredebut.strftime("%Y-%m-%d %H:%M:%S"),
                    'end': c.heurefin.strftime("%Y-%m-%d %H:%M:%S"),
                    'lieux': c.lieu,
                    'name': c.title,
                    'eleve': eleve.nom,
                    'heurePayee': heure.heurePaye,
                    'heureRestante': heure.heureRestant,
                    'inspecteur': c.inspecteur.nom,
                }
            else:
                event = {
                    'id': c.id,
                    'user': "secretaire",
                    'title': eleve.nom,
                    'start': c.heuredebut.strftime("%Y-%m-%d %H:%M:%S"),
                    'end': c.heurefin.strftime("%Y-%m-%d %H:%M:%S"),
                    'lieux': c.lieu,
                    'name': c.title,
                    'eleve': eleve.nom,
                    'heurePayee': '0',
                    'heureRestante': '0',
                    'inspecteur': c.inspecteur.nom,
                }
            events.append(event)
        context = {'events': events, 'timenow': timezone.now()}
        return render(request, 'auto_ecole/profil.html', context)
    else:
         messages.error(request, "Vous n'avez pas accès à cette page.")
         return redirect('login')

def rdv_delete(request, pk):
    event = get_object_or_404(Cours, pk=pk)
    heure = Heure.objects.first()
    duration = event.heurefin - event.heuredebut
    duration_in_hours = duration.seconds // 3600 + duration.days * 24
    heure.heureRestant += duration_in_hours
    heure.save()
    event.delete()
    
    return redirect('profile')

def rdv_update(request, pk):
    cours = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        form = CoursUpdateForm(request.POST, instance=cours)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le cours a bien été modifié.')
            return redirect('profile')
    else:
        form = CoursUpdateForm(instance=cours)
    return render(request, 'auto_ecole/update_rdv.html', {'form': form, 'cours': cours})

@login_required
def ajouter_rdv(request):
    utilisateur = User_profil.objects.get(email=request.user.email)
    if Secretaire.objects.filter(email=utilisateur.email).exists() or Inspecteur.objects.filter(email=utilisateur.email).exists() or request.user.is_superuser:
        if request.method == 'POST':
            form = RDVForm(request.POST)
            if form.is_valid():
                eleve = form.cleaned_data['eleve']
                inspecteur = eleve.inspecteur
                if 'inspecteur' in request.POST:
                    inspecteur = form.cleaned_data['inspecteur']
                date = form.cleaned_data['date']
                heure = form.cleaned_data['heure']
                if not inspecteur.disponible(date, heure):
                    messages.error(request, "L'inspecteur n'est pas disponible à cette heure-là.")
                    return redirect('ajouter_rdv')
                rdv = RendezVous.objects.create(eleve=eleve, inspecteur=inspecteur, date=date, heure=heure)
                messages.success(request, f"Le rendez-vous pour {eleve} avec {inspecteur} a été ajouté avec succès.")
                return redirect('liste_rdv')
            else:
                messages.error(request, "Veuillez remplir correctement le formulaire.")
        else:
            form = RDVForm()
        eleves = Eleve.objects.all()
        return render(request, 'auto_ecole/ajouter_rdv.html', {'form': form, 'eleves': eleves})
    else:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('profile')


def index(request):
    if request.user.is_superuser or Secretaire.objects.filter(user=request.user.id).exists() or Inspecteur.objects.filter(user=request.user.id).exists() or Eleve.objects.filter(user=request.user.id).exists():
        cours = Cours.objects.all()
    elif hasattr(request.user, 'eleves') and request.user.eleves:
        cours = Cours.objects.filter(eleve=request.user.eleve)
    elif hasattr(request.user, 'inspecteur') and request.user.inspecteur:
        cours = Cours.objects.filter(inspecteur=request.user.inspecteur)
    else:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('login')
    return render(request, 'auto_ecole/index.html', {'cours': cours})

@login_required
def ajout_inspecteur(request):
    utilisateur = User_profil.objects.get(email=request.user.email)
    if request.user.is_superuser or Secretaire.objects.filter(email=request.user.email).exists():
        if request.method == 'POST':
            form = InspecteurForm(request.POST)
            if form.is_valid():
                chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                password = ''.join(random.choice(chars) for i in range(8))
                user = User_profil(username=form.cleaned_data['nom'], email=form.cleaned_data['email'], first_name=form.cleaned_data['nom'], last_name=form.cleaned_data['prenom'], Inspecteurs=True)
                user.set_password(password)
                user.save()
                Inspecteur.objects.create(user=user, nom=form.cleaned_data.get('nom'), prenom=form.cleaned_data.get('prenom'), email=form.cleaned_data.get('email'))
                subject = "Mot de passe pour votre compte"
                message = f"Bonjour {form.cleaned_data['nom']}, votre mot de passe est {password} Merci de vous connetez afin de nous indiquer vos disponibilite"
                send_mail(
                    subject,
                    message,
                    'habyruffier@gmail.com',
                    [form.cleaned_data['email']],
                    fail_silently=False,
                )
                messages.success(request, "Inspecteur ajouté avec succès. Un e-mail avec le mot de passe a été envoyé à l'adresse e-mail donner.")
                return redirect('profile')
        else:
            form = InspecteurForm()
        return render(request, 'auto_ecole/ajout_inspecteur.html', {'form': form})
    else:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('profile')
    
@login_required
def ajout_secretaire(request):
    utilisateur = User_profil.objects.get(email=request.user.email)
    if request.user.is_superuser or Secretaire.objects.filter(email=request.user.email).exists():
        if request.method == 'POST':
            form = SecretaireForm(request.POST)
            if form.is_valid():
                chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                password = ''.join(random.choice(chars) for i in range(8))
                user = User_profil(username=form.cleaned_data['nom'], email=form.cleaned_data['email'], first_name=form.cleaned_data['nom'], last_name=form.cleaned_data['prenom'], Secretaires=True, numero=form.cleaned_data['numero'])
                user.set_password(password)
                user.save()
                Secretaire.objects.create(user=user, nom=form.cleaned_data.get('nom'), prenom=form.cleaned_data.get('prenom'), email=form.cleaned_data.get('email'))
                subject = "Mot de passe pour votre compte"
                message = f"Bonjour {form.cleaned_data['nom']}, votre mot de passe est {password}"
                send_mail(
                    subject,
                    message,
                    'habyruffier@gmail.com',
                    [form.cleaned_data['email']],
                    fail_silently=False,
                )
                messages.success(request, "Secretaire ajouté avec succès. Un e-mail avec le mot de passe a été envoyé à l'adresse e-mail donner.")

                return redirect('profil')
        else:
            form = SecretaireForm()
        return render(request, 'auto_ecole/ajout_secretaire.html', {'form': form})
    else:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('profile')

@login_required
def ajout_eleve(request):
    utilisateur = User_profil.objects.get(email=request.user.email)
    if request.user.is_superuser or Secretaire.objects.filter(email=request.user.email).exists():
        if request.method == 'POST':
            form = EleveForm(request.POST)
            if form.is_valid():
                chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
                password = ''.join(random.choice(chars) for i in range(8))
                user = User_profil(username=form.cleaned_data['nom'], email=form.cleaned_data['email'], first_name=form.cleaned_data['nom'], last_name=form.cleaned_data['prenom'], Eleves=True)
                user.set_password(password)
                user.save()
                incritpion = Inspecteur.objects.all()
                inspecteurs = random.choice(incritpion)
                Eleve.objects.create(user=user, nom=form.cleaned_data.get('nom'), prenom=form.cleaned_data.get('prenom'), email=form.cleaned_data.get('email'), inspecteur=inspecteurs)
                subject = "Mot de passe pour votre compte"
                message = f"Bonjour {form.cleaned_data['nom']}, votre mot de passe est '{password}'. Merci de vous connetez afin de nous indiquer vos disponibilite"
                send_mail(
                    subject,
                    message,
                    'habyruffier@gmail.com',
                    [form.cleaned_data['email']],
                    fail_silently=False,
                )
                messages.success(request, "Élève ajouté avec succès. Un e-mail avec le mot de passe a été envoyé à l'adresse e-mail de l'élève.")
                return redirect('heure_paye')
        else:
            form = EleveForm()
        return render(request, 'auto_ecole/ajout_eleve.html', {'form': form})
    else:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('profile')

@login_required
def ajout_cours(request):
    utilisateur = User_profil.objects.get(email=request.user.email)
    if request.user.is_superuser or Secretaire.objects.filter(email=request.user.email).exists() or Inspecteur.objects.filter(email=request.user.email).exists():
        if request.method == 'POST':
            form = CoursForm(request.POST, user=request.user)
            if form.is_valid():
                cours = form.save(commit=False)
                eleves = form.cleaned_data['eleve']
                inspecteur = form.cleaned_data['inspcteur']
                heuredebut = form.cleaned_data['heuredebut']
                if isinstance(eleves, Eleve):
                    cours.eleve = eleves
                    heuredispo_str = str(eleves.heuredispo) + ':00'
                    heuredispo_time = datetime.datetime.strptime(heuredispo_str, '%H:%M').time()
                    heureindispo_str = str(eleves.heureindispo) + ':00'
                    heureindispo_time = datetime.datetime.strptime(heureindispo_str, '%H:%M').time()
                    eleve_disponible = eleves.heuredispo and eleves.heureindispo and  heuredispo_time <= heuredebut.time() <= heureindispo_time
                    if not eleve_disponible:
                        messages.error(request, "L'élève n'est pas disponible à cette heure.")
                        return redirect('ajout_cours')
                if isinstance(inspecteur, Inspecteur):
                    cours.inspecteur = inspecteur
                    print(cours.heuredebut)
                    heuredispoin_str = str(inspecteur.heuredispo) + ':00'
                    heuredispoin_time = datetime.datetime.strptime(heuredispoin_str, '%H:%M').time()
                    heureindispoin_str = str(inspecteur.heureindispo) + ':00'
                    heureindispoin_time = datetime.datetime.strptime(heureindispoin_str, '%H:%M').time()
                    inspecteur_disponible = inspecteur.heuredispo and inspecteur.heureindispo and  heuredispoin_time <= heuredebut.time() <= heureindispoin_time
                    if not inspecteur_disponible:
                        messages.error(request, "L'inspecteur n'est pas disponible à cette heure.")
                        return redirect('ajout_cours')
                    if Inspecteur.objects.filter(email=request.user.email).exists():
                        inspecteur = Inspecteur.objects.get(email=request.user.email)
                    else:
                        if eleves.inspecteur == form.cleaned_data['inspcteur']:
                          inspecteur = eleves.inspecteur
                        else:
                            inspecteur = form.cleaned_data['inspcteur']
                            Elevetemp = Eleve.objects.get(email=eleves.email)
                            Elevetemp.inspecteur = inspecteur
                            Elevetemp.save()
                            
                    cours.inspecteur = inspecteur
                    cours.heuredebut = form.cleaned_data['heuredebut']
                    cours.heurefin = form.cleaned_data['heurefin']
                    if Cours.objects.filter(heuredebut=cours.heuredebut, inspecteur=inspecteur).exists():
                        messages.error(request, "L'inspecteur est déjà occupé à cette heure.")
                    else:
                      if Heure.objects.filter(user=eleves).exists():
                          heure_payee = Heure.objects.get(user=eleves)
                          if heure_payee.heureRestant == None or heure_payee.heureRestant == 0:
                              heure_payee.heureRestant = heure_payee.heurePaye
                              heure_payee.save()
                              cours.save()
                              messages.success(request, "Cours de {eleve} ajouté avec succès. reste {heure_payee} h".format(eleve=eleves.nom, heure_payee=heure_payee.heureRestant))
                          elif heure_payee.heureRestant > 1:
                              if form.cleaned_data['une_heure']:
                                heure_payee.heureRestant -= 1
                                heure_payee.save()
                                cours.save()
                              elif form.cleaned_data['deux_heures']:
                                heure_payee.heureRestant -= 2
                                heure_payee.save()
                                cours.save()
                              elif form.cleaned_data['trois_heures']:
                                heure_payee.heureRestant -= 3
                                heure_payee.save()
                                cours.save()
                              messages.success(request, "Cours de {eleve} ajouté avec succès. reste {heure_payee} h".format(eleve=eleves.nom, heure_payee=heure_payee.heureRestant))
                          else:
                              messages.error(request, "Plus d'heure disponible. Veuillez ajouter des heures.")
                              return redirect('heure_paye')
                      else:
                          messages.error(request, "Plus d'heure disponible. Veuillez ajouter des heures.")
                          return redirect('heure_paye')
                else:
                    messages.error(request, "Impossible de trouver l'élève.")
                    return redirect('profile')
        else:
            form = CoursForm(user=request.user)
        return render(request, 'auto_ecole/ajout_cours.html', {'form': form})
    elif Eleve.objects.filter(email=utilisateur.email).exists():
        messages.error(request, "Les élèves ne peuvent pas ajouter de cours. Veuillez contacter la secretaire.")
        return redirect('profile')
    else:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('index')

def planning(request, id):
    if request.user.is_superuser or Secretaire.objects.filter(email=request.user.email).exists():
        utilisateur= User_profil.objects.get(id=id)
        if utilisateur.Inspecteurs == True:
          Inspecteurs = Inspecteur.objects.get(user_id=id)
          cours = Cours.objects.all()
          course = cours.filter(inspecteur_id=Inspecteurs.id)
          events = []
          for c in course:
              eleve = c.eleve
              heure = Heure.objects.filter(user=eleve).first()
              if heure is None:
                  print(f"No Heure object found for Eleve {eleve}")
              else:
                  event = {
                      'id': c.id,
                      'user': "secretaire",
                      'title': heure.user.nom,
                      'start': c.heuredebut,
                      'end': c.heurefin,
                      'lieux': c.lieu,
                      'name': c.title,
                      'eleve': eleve.nom,
                      'heurePayee': heure.heurePaye,
                      'heureRestante': heure.heureRestant,
                      'inspecteur': Inspecteurs.nom,
                  }
                  events.append(event)
              JsonResponse(events, safe=False)
              return render(request, 'auto_ecole/planning.html', {'events': cours})
        elif utilisateur.Eleves == True:
          eleve = Eleve.objects.get(user_id=id)
          cours = Cours.objects.all()
          course = cours.filter(eleve_id=eleve.id)
          Inspecteurs = Inspecteur.objects.all()
          heure = Heure.objects.all()
          HeurePayee = heure.filter(user=eleve)
          events = []
          for c in course:
              eleve = c.eleve
              heure = Heure.objects.filter(user=eleve).first()
              if heure is None or heure.heureRestant is None:
                  event = {
                  'id': c.id,
                  'user': "eleve",
                  'title': c.title,
                  'start': c.heuredebut,
                  'end': c.heurefin,
                  'lieux': c.lieu,
                  'name': c.title,
                  'eleve': eleve.nom,
                  'heurePayee': heure.heurePaye,
                  'heureRestante': 0,
                  'inspecteur': heure.user.inspecteur.nom,
              }
              else:
               event = {
                  'id': c.id,
                  'user': "eleve",
                  'title': c.title,
                  'start': c.heuredebut,
                  'end': c.heurefin,
                  'lieux': c.lieu,
                  'name': c.title,
                  'eleve': eleve.nom,
                  'heuresPayee': heure.heurePaye,
                  'heuresRestante': heure.heureRestant,
                  'inspecteur': heure.user.inspecteur.nom,
              }
              events.append(event)
          JsonResponse(events, safe=False)
          return render(request, 'auto_ecole/planning.html', {'events': events})
        else:
            messages.error(request, "Pas de cours planifié")
            return redirect('profile')
    else:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('profile')
    
def planningjson(request, id):
    if request.user.is_superuser or Secretaire.objects.filter(email=request.user.email).exists():
        utilisateur= User_profil.objects.get(id=id)
        if utilisateur.Inspecteurs == True:
          Inspecteurs = Inspecteur.objects.get(user_id=id)
          cours = Cours.objects.all()
          course = cours.filter(inspecteur_id=Inspecteurs.id)
          events = []
          for c in course:
              eleve = c.eleve
              heure = Heure.objects.filter(user=eleve).first()
              if heure is None:
                  print(f"No Heure object found for Eleve {eleve}")
              else:
                  event = {
                      'id': c.id,
                      'user': "secretaire",
                      'title': heure.user.nom,
                      'start': c.heuredebut,
                      'end': c.heurefin,
                      'lieux': c.lieu,
                      'name': c.title,
                      'eleve': eleve.nom,
                      'heurePayee': heure.heurePaye,
                      'heureRestante': heure.heureRestant,
                      'inspecteur': Inspecteurs.nom,
                  }
              events.append(event)
          return JsonResponse(events, safe=False)
        elif utilisateur.Eleves == True:
          eleve = Eleve.objects.get(user_id=id)
          cours = Cours.objects.all()
          course = cours.filter(eleve_id=eleve.id)
          Inspecteurs = Inspecteur.objects.all()
          heure = Heure.objects.all()
          HeurePayee = heure.filter(user=eleve)
          events = []
          for c in course:
              eleve = c.eleve
              heure = Heure.objects.filter(user=eleve).first()
              if heure is None or heure.heureRestant is None:
                  event = {
                  'id': c.id,
                  'user': "eleve",
                  'title': c.title,
                  'start': c.heuredebut,
                  'end': c.heurefin,
                  'lieux': c.lieu,
                  'name': c.title,
                  'eleve': eleve.nom,
                  'heurePayee': heure.heurePaye,
                  'heureRestante': 0,
                  'inspecteur': heure.user.inspecteur.nom,
              }
              else:
               event = {
                  'id': c.id,
                  'user': "eleve",
                  'title': c.title,
                  'start': c.heuredebut,
                  'end': c.heurefin,
                  'lieux': c.lieu,
                  'name': c.title,
                  'eleve': eleve.nom,
                  'heuresPayee': heure.heurePaye,
                  'heuresRestante': heure.heureRestant,
                  'inspecteur': heure.user.inspecteur.nom,
              }
              events.append(event)
          return JsonResponse(events, safe=False)
        else:
            messages.error(request, "Impossible de trouver l'élève.")
            return redirect('profile')
    else:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('profile')

def heure_dispo(request, id):
    if Eleve.objects.filter(user=request.user).exists():
      eleve = get_object_or_404(Eleve, id=id)
      if request.method == 'POST':
          form = HeureDispoForm(request.POST)
          if form.is_valid():
              heuredispo = form.cleaned_data['heuredispo']
              heureindispo = form.cleaned_data['heureindispo']
              if heuredispo and heureindispo:
                  # Vérification de l'ordre des heures
                  if heureindispo <= heuredispo:
                      messages.error(request, "L'heure de fin de disponibilité doit être après l'heure de début.")
                      return redirect('update_heure_dispo', id=id)
                  # Ajout des nouvelles heures de disponibilité
                  eleve.heuredispo = heuredispo
                  eleve.heureindispo = heureindispo
                  eleve.save()
                  messages.success(request, "Vos heures de disponibilité ont été mises à jour avec succès.")
                  return redirect('eleve_detail', id=id)
      else:
          form = HeureDispoForm()
      return render(request, 'auto_ecole/heuredispo.html', {'form': form})
    elif Inspecteur.objects.filter(user=request.user).exists():
      inspecteur = get_object_or_404(Inspecteur, id=id)
      if request.method == 'POST':
          form = HeureDispoFormInspecteur(request.POST)
          if form.is_valid():
              heuredispo = form.cleaned_data['heuredispo']
              heureindispo = form.cleaned_data['heureindispo']
              if heuredispo and heureindispo:
                  # Vérification de l'ordre des heures
                  if heureindispo <= heuredispo:
                      messages.error(request, "L'heure de fin de disponibilité doit être après l'heure de début.")
                      return redirect('update_heure_dispo', id=id)
                  
                  # Ajout des nouvelles heures de disponibilité
                  inspecteur.heuredispo = heuredispo
                  inspecteur.heureindispo = heureindispo
                  inspecteur.save()
                  messages.success(request, "Vos heures de disponibilité ont été mises à jour avec succès.")
                  return redirect('inspecteur_detail', id=id)
      else:
          form = HeureDispoFormInspecteur()
      return render(request, 'auto_ecole/heuredispo.html', {'form': form})
  