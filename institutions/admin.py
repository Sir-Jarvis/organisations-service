from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(TypeOrganisation)
class TypeOrganisationAdmin(admin.ModelAdmin):
    list_display=('nom',)


"""N'oublions pas les contrats aue l'admin, l'intitution et l'élève puisse le voir"""
@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('id','nom','localite','numero_portable','numero_fixe','logo','typeOrganisation')


@admin.register(SousDemande)
class SousDemandeAdmin(admin.ModelAdmin):
    list_display = ('id','typeStage','niveau','duree')


@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):
    list_display = ('id','debut','fin','user','dateDemande')

@admin.register(UrlsInstitutionDemande)
class UrlsInstitutionDemandeAdmin(admin.ModelAdmin):
    list_display = ('fileUrl','institution','demande')


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('id','debut','fin','sousDemande','nombre','dateCreated')



@admin.register(AppelACandidature)
class AppelACandidatureAdmin(admin.ModelAdmin):
    list_display = ('id','typeStage','debut','fin','institution','nombre','dureeStage')

@admin.register(ContenuProjet)
class ContenuProjetAdmin(admin.ModelAdmin):
    list_display=('id','projetName','description')

@admin.register(ActiviteContenu)
class ActiviteContenuAdmin(admin.ModelAdmin):
    list_display=('id','nomActivite','contenu')


    


    






