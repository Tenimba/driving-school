from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    InspecteurViewSet,
    EleveViewSet,
    CoursViewSet,
    SecretaireViewSet,
    index,
    ajout_inspecteur,
    ajout_eleve,
    ajout_cours,
    inscription,
    connexion,
    profil,
    ispecteur_list,
    eleve_list,
    delete_eleve,
    eleve_detail,
    ajouterheure,
    cours_list,
    secretaire_list,
    inspecteur_detail,
    deconnexion,
    delete_inscpetur,
    rdv_delete,
    rdv_update,
    planning,
    planningjson,
    secretaire_detail,
    secretaire_delete,
    heure_dispo,
    ajout_secretaire,

)

router = DefaultRouter()
router.register('inspecteur', InspecteurViewSet, basename='inspecteur')
router.register('eleve', EleveViewSet, basename='eleve')
router.register('cours', CoursViewSet, basename='cours')
router.register('secretaire', SecretaireViewSet, basename='secretaire')

urlpatterns = [
    path('index/', index, name='index'),
    path('api/', include(router.urls), name='api'),
    path('ajout_inspecteur/', ajout_inspecteur, name='ajout_inspecteur'),
    path('ajout_eleve/', ajout_eleve, name='ajout_eleve'),
    path('ajout_cours/', ajout_cours, name='ajout_cours'),
    path('accounts/login/', connexion, name='logins'),
    path('login/', connexion, name='logins'),
    path('', connexion, name='login'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('logout/', LogoutView.as_view(template_name='auto_ecole/login.html'), name='logout'),
    path('inscription/', inscription, name='inscription'),
    path('profile/', profil, name='profile'),
    path('inspecteur_list/', ispecteur_list, name='inspecteur_list'),
    path('eleve_list/', eleve_list, name='eleve_list'),
    path('eleve/delete/<int:id>/', delete_eleve, name='delete_eleve'), # add this line
    path('eleve/<int:id>', eleve_detail, name='eleve_detail'),
    path('rdv_json/', cours_list, name='cours_list'),
    path('rdv/<int:id>', planningjson, name='cours_list'),
    path('secretaire_list/', secretaire_list, name='secretaire_list'),
    path('heure_paye/', ajouterheure, name='heure_paye'),
    path('inspecteur/<int:id>', inspecteur_detail, name='inspecteur_detail'),
    path('delete_inspecteur/<int:id>/', delete_inscpetur, name='delete_inspecteur'),
    path('rdv/delete/<int:pk>', rdv_delete, name='rdv_delete'),
    path('rdv/update/<int:pk>', rdv_update, name='rdv_update'),
    path('planning/<int:id>', planning, name='planning'),
    path('secretaire/<int:id>', secretaire_detail, name='secretaire_detail'),
    path('secretaire/delete/<int:id>/', secretaire_delete, name='secretaire_delete'),
    path('disponibilite/<int:id>', heure_dispo, name='disponibilite'),
    path('ajout_secretaire/', ajout_secretaire, name='ajout_secretaire'),
]
