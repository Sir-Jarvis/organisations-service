from django.http import Http404
from .models import *
from rest_framework import serializers


class ActiviteContenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiviteContenu
        fields = "__all__"


class ActiviteContenuCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiviteContenu
        fields = "__all__"
    
    def create(self,validated_data):
        activite = ActiviteContenu.objects.create(**validated_data)
        activite.save()
        return activite


class ContenuProjetSerializer(serializers.ModelSerializer):
    activite = ActiviteContenuSerializer(many=True)

    class Meta:
        model = ContenuProjet
        depth = 1
        fields = "__all__"



class TypeOrganisationSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TypeOrganisation
        depth = 1
        fields = "__all__"


class InstitutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        depth = 1
        fields = "__all__"

class OffreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offre
        depth = 2
        fields = "__all__"

class OffreCreateSerializer(serializers.ModelSerializer):
    contenu = ContenuProjetSerializer(many=True)

    class Meta:
        model = Offre
        fields = ('id','debut','fin','sousDemande','nombre','dateCreated','contenu')

    def get_institution(self,id):
        try:
            return Institution.objects.get(id=id)
        except:
            raise Http404("Cette institution n'existe pas!")

    def get_sousDemande(self,id):
        try:
            return SousDemande.objects.get(id=id)
        except SousDemande.DoesNotExist:
            return None

    def create(self,validated_data):
        #self.get_institution(validated_data['institution'])
        #self.get_sousDemande(validated_data['sousDemande'])
        contenu = validated_data.pop['contenu']
        offre = Offre.objects.create(**validated_data)
        offre.save()
        return offre



class UrlsInstitutionDemandeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UrlsInstitutionDemande
        depth=1
        fields = "__all__"


class UrlsInstDemandeCreateSerializer(serializers.ModelSerializer): 

    class Meta:
        model = UrlsInstitutionDemande
        fields = "__all__"

    def get_institution(self,id):
        try:
            return Institution.objects.get(id=id)
        except:
            raise Http404("Cette institution n'existe pas!")

    def get_demande(self,id):
        try:
            return Demande.objects.get(id=id)
        except:
            raise Http404("Cette demande n'existe pas!")

    def create(self,validated_data):
        #self.get_institution(id=validated_data['institution'])
        #self.get_demande(id=validated_data['demande'])
        urlsFile = UrlsInstitutionDemande.objects.create(**validated_data)
        urlsFile.save()
        return urlsFile
    
    

class SousDemandeSerializer(serializers.ModelSerializer):
    offres=OffreSerializer(many=True,read_only=True)

    class Meta:
        model = SousDemande
        fields = ('typeStage','niveau','duree','offres','demande')

    



class SousDemandeCreateSerializer(serializers.ModelSerializer):
    offres = OffreSerializer(many=True)

    class Meta:
        model = SousDemande
        fields = ('typeStage','niveau','duree','offres')



class DemandeSerializer(serializers.ModelSerializer):
    files = UrlsInstitutionDemandeSerializer(many=True)

    class Meta:
        model = Demande
        depth = 4
        fields = "__all__"
        

    

class DemandeCreateSerializer(serializers.ModelSerializer):
    # sousdemande = sousdemandeerializer(read_only=True, many=True)
    sousDemandes = SousDemandeCreateSerializer(many=True,read_only=True)
    institutions = serializers.ListField(child=serializers.IntegerField())
    """create contenu"""

    
    class Meta:
        model = Demande
        fields = ('debut','fin','user','sousDemandes', 'institutions')

    def get_instutition(self,id):
        try:
            return Institution.objects.get(id=id)
        except:
            raise Http404("Cette institution n'existe pas!")

    def get_user(self,id):
        try:
            user = requests.get('http://127.0.0.1:8081/api/auth/users/{id}')
            return user
        except:
            raise Http404("Cet utilisateur n'existe pas!")

    def create(self, validated_data):
        #self.get_user(validated_data["user"])
        sousdemandes_data = validated_data.pop('sousDemandes')
        institutions = validated_data.pop('institutions')
        demande = Demande.objects.create(**validated_data)

        for sd in sousdemandes_data:
            SousDemande.objects.create(demande=demande,**sd)

        for idInst in institutions:
            institution = self.get_instutition(idInst)
            demande.institutions.add(institution)
            demande.save()

        return demande


    def update(self,instance,validated_data):
        print(validated_data)
        sousdemandes_data = validated_data.pop('sousDemandes')
        print(sousdemandes_data)
        institutions = validated_data.pop('institutions')
        for item in validated_data:
            if Demande._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        SousDemande.objects.filter(demande=instance).delete() 
        Institution.objects.filter(demande=instance).delete()

        for sd in sousdemandes_data:
            SousDemande.objects.create(demande=instance, **sd)
        instance.save()

        for idInst in institutions:
            demande.institution.add(instance)
        institution.save()

        return instance


class AppelACandidatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppelACandidature
        depth = 1
        fields = "__all__"

class AppelsACandidatureCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppelACandidature
        fields="__all__"

    def get_instutition(self,id):
        try:
            return Institution.objects.get(id=id)
        except:
            raise Http404("Cette institution n'existe pas!")

    def create(self,validated_data):
        appelACandidature = AppelACandidature.objects.create(**validated_data)
        return appelACandidature



class ContenuCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContenuProjet
        fields = "__all__" 

    def create(self,validated_data):
        contenu = ContenuProjet.objects.create(**validated_data)
        return contenu

  

        
        

            
