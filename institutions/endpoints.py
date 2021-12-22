from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'institution', InstitutionViewSet, basename='institution')


# urlpatterns = router.urls 
# urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('institutions/', InstitutionAPIView.as_view()),
    path('institutions/<int:id>/', InstitutionDetailAPIView.as_view()),
    path('demandes/',DemandeAPIView.as_view()),
    path('demandes/<int:id>/',DemandeDetailAPIView.as_view()),
    path('offres/',OffreAPIView.as_view()),
    path('offres/<int:id>/',OffreDetailAPIView.as_view()),
    path('offres/sousDemande/<int:id>/',OffreSousDemandeAPIView.as_view()),
    path('sousDemandes/<int:id>/',SousDemandeAPIView.as_view()),
    path('demandes/institution/<int:id>/',DemandeInstAPIView.as_view()),
    path('urlsFilesDemandesInst/',UrlsInstitutionDemandeAPIView.as_view()),
    path('appelsACandidatures/',AppelACandidatureAPIView.as_view()),
    path('appelsACandidatures/institution/<int:id>/',AppelACandidatureInstAPIView.as_view()),
    path('appelsACandidatures/<int:id>/',AppelACandidatureDetailAPIView.as_view()),
    path('appelsACandidatures/<int:id>/contenu',ContenuAPIView.as_view()),
    path('contenu/<int:id>',ContenuDetailProjet.as_view()),
    path('contenu/<int:id>/activites',ActiviteAPIView.as_view()),
    path('activites/<int:id>',ActiviteDetailAPIView.as_view()),
    path('offres/<int:id>/contenu',ContenuOffreAPIView.as_view()),

    
    #get offre selon sousDemande

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
