from django.shortcuts import render
from rest_framework import status, permissions,viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from .models import *
from rest_framework import generics
from .serializers import *
import requests
import json



#implementation de methodes pour Institutions

@permission_classes((permissions.AllowAny,))
class InstitutionAPIView(APIView):

    def get(self,request,*args, **kwargs):
        institutions = Institution.objects.all()
        serializer = InstitutionSerializer(institutions,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,format=None,*args,**kwargs):
        parser_classes = (MultiPartParser,)


        data = {
            'nom' : request.data['nom'],
            'localite' : request.data['localite'],
            'numero_portable' : request.data['numero_portable'],
            'numero_fixe' : request.data['numero_fixe'],
            'description' : request.data['description'],
            'domaine_activites' : request.data['domaine_activites']
            # 'logo' : request.data['logo']
        }

        serializer = InstitutionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,))
class InstitutionDetailAPIView(APIView):

    def get_institution(self,id):
        try:
            return Institution.objects.get(id=id)
        except Institution.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):

        institution = self.get_institution(id)
        if not institution:
            return Response({"reponse":"Cette institution n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)

        serializer = InstitutionSerializer(institution)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,id,*args, **kwargs):
        institution = self.get_institution(id)
        if not institution:
            return Response({"reponse":"Cette institution n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)

        data = {
            'nom' : request.data['nom'],
            'localite' : request.data['localite'],
            'numero_portable' : request.data['numero_portable'],
            'numero_fixe' : request.data['numero_fixe'],
            'description' : request.data['description'],
            'domaine_activites' : request.data['domaine_activites'],
            'logo' : request.data['logo']
        }

        serializer = InstitutionSerializer(instance=institution, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id,format=None):
        institution = Institution.objects.get(id=id)
        if not institution:
            return Response({"reponse":"Cette institution n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)
        institution.delete()
        return Response({"reponse": "Suppression reussie!"},status=status.HTTP_200_OK)



@permission_classes((permissions.AllowAny,))
class DemandeAPIView(APIView):
    """
        Cette classe permet de gérér l ensemble des demandes.
        NB: Demande= Appel à proposition faite à une organisation
        get: Obtenir toutes les demandes
        post: creer une nouvelle demande

    """

    def get(self,request,*args, **kwargs):
        demandes = Demande.objects.all()
        serializer = DemandeSerializer(demandes,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 
        
    def post(self,request,formate=None,*args, **kwargs):       
        serializer = DemandeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        demande = serializer.save()
        return Response(DemandeSerializer(demande).data, status=status.HTTP_201_CREATED)
        


@permission_classes((permissions.AllowAny,))
class DemandeDetailAPIView(APIView):
    """
        get: Obtenir les details d'une demande selon son id
        put: mettre à jour les informations d'une demande donnée
        delete: supprimer une demande
    """

    def get_demande(self,id):
        try:
            return Demande.objects.get(id=id)
        except Demande.DoesNotExist:
            return None 

    def get(self,request,id,*args, **kwargs):
        demande = self.get_demande(id=id)
        if not demande:
            return Response({"reponse":"Cette demande n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)

        serializer = DemandeSerializer(demande)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self,request,id,*args, **kwargs):
        demande = self.get_demande(id=id)
        if not demande:
            return Response({"reponse":"Cette demande n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)

        data={
            "sousDemandes":request.data['sousDemandes'],
            "user":request.data['user'],
            "debut":request.data['debut'],
            "fin":request.data['fin'],
            "institutions":request.data['institutions']
        }
        
        serializer = DemandeCreateSerializer(instance=demande,data=data,partial=True)
        serializer.is_valid(raise_exception=True,partial=True)
        demande = serializer.save()
        return Response(DemandeSerializer(demande).data, status=status.HTTP_201_CREATED)


    
    def delete(self,request,id,format=None):
        demande = self.get_demande(id=id)
        if not demande:
            return Response({"reponse":"Cette demande n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)
        demande.delete()
        return Response({"reponse": "Suppression reussie!"},status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class DemandeInstAPIView(APIView):
    """
    get: récupérer une demande qui concerne une institution donnée
    """
    def get_institution(self,id):
        try:
            return Institution.objects.get(id=id)
        except Institution.DoesNotExist:
            return None
    def get(self,request,id,*args, **kwargs):
        institution=self.get_institution(id=id)
        if not institution:
            return Response({"response":"cette institution n'existe pas"},status=status.HTTP_400_BAD_REQUEST)
        demandes = Demande.objects.filter(institutions=id)
        serializer = DemandeSerializer(demandes,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



@permission_classes((permissions.AllowAny,))
class OffreAPIView(APIView):
    """
    get: récupérer toutes les offres
    NB: une offre concerne une demande particuliere (une sous-demande d'une demande)
    post: créer une nouvelle offre

    """

    def get(self,request,*args, **kwargs):
        offres = Offre.objects.all()
        serializer = OffreSerializer(offres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

    def post(self,request,format=None,*args, **kwargs):
        serializer = OffreCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        offre = serializer.save()
        return Response(OffreSerializer(offre).data, status=status.HTTP_201_CREATED)




@permission_classes((permissions.AllowAny,))
class OffreDetailAPIView(APIView):
    """
        get: récupérer les détails d'une offre donnée selon son id
    """
    def get_offre(self,id):
        try:
            return Offre.objects.get(id=id)
        except Offre.DoesNotExist:
            return None 

    def get(self,request,id,*args, **kwargs):
        offre = self.get_offre(id=id)
        if not offre:
            return Response({"reponse":"Cette offre n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)

        serializer = OffreSerializer(offre)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self,request,id,format=None):
        offre = self.get_offre(id=id)
        if not offre:
            return Response({"reponse":"Cette offre n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)
        offre.delete()
        return Response({"reponse": "Suppression reussie!"},status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class OffreSousDemandeAPIView(APIView):
    """
        get: Obtenir l'offre d'une organisation selon une sous-demande donnée

    """

    def getSousDemande(self,id):
        try:
            return SousDemande.objects.get(id=id)
        except SousDemande.DoesNotExist:
            return None

    # def getOffre(self,idOffre):
    #     try:
    #         return Offre.objects.get(id=idOffre)
    #     except Offre.DoesNotExist:
    #         return None 

    def get(self,request,id,*args, **kwargs):
        sousDemande = self.getSousDemande(id=id)
        if not sousDemande:
            return Response({"reponse":"Cette sous-demande n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)
        sousDemande = Offre.objects.filter(sousDemande=id)
        serializer = OffreSerializer(sousDemande,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    



@permission_classes((permissions.AllowAny,))
class SousDemandeAPIView(APIView):
    schema = None
    def get_sousDemande(self,id):
        try:
            return SousDemande.objects.filter(demande=id)
        except SousDemande.DoesNotExist:
            return None 

    def get(self,request,id,*args, **kwargs):
        sd = SousDemande.objects.filter(demande=id)
        serializer = SousDemandeSerializer(sd,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class UrlsInstitutionDemandeAPIView(APIView):
    """
        cette classe regroupe l'ensemble des liens des fichiers concernant une demande et une institution donnée
        get: récupérer les liens des fichiers d'une demande
        post: créer un nouveau fichier demande-institution.
        Pour le post il faudra envoyer le fichier pdf concerné!

    """
    parser_classes = (MultiPartParser,)


    def get(self,request,*args, **kwargs):
        urlsFiles = UrlsInstitutionDemande.objects.all()
        serializer = UrlsInstitutionDemandeSerializer(urlsFiles,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        f=request.FILES['file']
        print(f"le fichier a upload est: {f}")
        r = requests.post('http://127.0.0.1:8081/uploadFile', files={'file':f})
        resp = json.loads(r.text)
        data = {
            'institution':request.data['institution'],
            'demande':request.data['demande'],
            'fileUrl':resp['url']
        }

        serializer = UrlsInstDemandeCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        urlsFile = serializer.save()
        return Response(UrlsInstitutionDemandeSerializer(urlsFile).data, status=status.HTTP_201_CREATED)


@permission_classes((permissions.AllowAny,))
class AppelACandidatureAPIView(APIView):
    """
    get: récupérer l'ensemble des appels à candidatures faites par les entreprises
    post: pour une institution, créer une nouvelle offre

    """

    def get(self,request,*args, **kwargs):
        appelsACandidatures = AppelACandidature.objects.all()
        serializer = AppelACandidatureSerializer(appelsACandidatures,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        serializer = AppelsACandidatureCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appels = serializer.save()
        return Response(AppelACandidatureSerializer(appels).data,status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class AppelACandidatureInstAPIView(APIView):
    """
        get: récupérer une offre faites par une institution particuliere
    """

    def get_institution(self,id):
        try:
            return Institution.objects.get(id=id)
        except Institution.DoesNotExist:
            return None
    def get(self,request,id,*args, **kwargs):
        institution=self.get_institution(id=id)
        if not institution:
            return Response({"response":"cette institution n'existe pas"},status=status.HTTP_400_BAD_REQUEST)
        
        appels = AppelACandidature.objects.filter(institution=id)
        serializer = AppelACandidatureSerializer(appels,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

@permission_classes((permissions.AllowAny,))
class AppelACandidatureDetailAPIView(APIView):
    """
        get: récupérer une offre précise
    """
    def get_appel(self,id):
        try:
            return AppelACandidature.objects.get(id=id)
        except AppelACandidature.DoesNotExist:
            return None
    def get(self,request,id,*args, **kwargs):
        appel=self.get_appel(id=id)
        if not appel:
            return Response({"response":"cet appel à candidature  n'existe pas"},status=status.HTTP_400_BAD_REQUEST)
        appel = AppelACandidature.objects.get(id=id)
        serializer = AppelACandidatureSerializer(appel)
        return Response(serializer.data,status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class ContenuAPIView(APIView):

    def get_appelACandidature(self,id):
        try:
            return AppelACandidature.objects.get(id=id)
        except AppelACandidature.DoesNotExist:
            return None

    def get(self,request,id,*args, **kwargs):
        appel = self.get_appelACandidature(id=id)
        if not appel:
            return Response({"reponse":"Cet appel à proposition 'existe pas!"},status=status.HTTP_400_BAD_REQUEST)
        contenu = ContenuProjet.objects.filter(appelACandidature=id)
        serializer = ContenuProjetSerializer(contenu,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        serializer = ContenuCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contenu = serializer.save()
        return Response(ContenuProjetSerializer(contenu).data,status=status.HTTP_200_OK)



@permission_classes((permissions.AllowAny,))
class ContenuOffreAPIView(APIView):

    def get_offre(self,id):
        try:
            return Offre.objects.get(id=id)
        except Offre.DoesNotExist:
            return None

    def get(self,request,id,*args, **kwargs):
        offre = self.get_offre(id=id)
        if not offre:
            return Response({"reponse":"Cet offre à proposition 'existe pas!"},status=status.HTTP_400_BAD_REQUEST)
        contenu = ContenuProjet.objects.filter(offre=id)
        serializer = ContenuProjetSerializer(contenu,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        serializer = ContenuCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contenu = serializer.save()
        return Response(ContenuProjetSerializer(contenu).data,status=status.HTTP_200_OK)






@permission_classes((permissions.AllowAny,))
class ContenuDetailProjet(APIView):

    def get_contenu(self,id):
        try:
            return ContenuProjet.objects.get(id=id)
        except ContenuProjet.DoesNotExist:
            return None

    def get(self,request,id,*args, **kwargs):
        contenu = self.get_contenu(id=id)
        if not contenu:
            return Response({"reponse":"Ce contenu n'existe pas!"})
        contenu = ContenuProjet.objects.get(id=id)
        serializer = ContenuProjetSerializer(contenu)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,id,*args, **kwargs):
        contenu = self.get_contenu(id=id)
        if not contenu:
            return Response({"reponse":"Ce contenu à candidature n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)
        serializer = ContenuCreateSerializer(instance=contenu,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        contenu = serializer.save()
        return Response(ContenuProjetSerializer(contenu).data, status=status.HTTP_201_CREATED)

    def delete(self,request,id,format=None):
        contenu = self.get_offre(id=id)
        if not offre:
            return Response({"reponse":"Ce contenu n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)
        contenu.delete()
        return Response({"reponse": "Suppression reussie!"},status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class ActiviteAPIView(APIView):

    def get_contenu(self,id):
        try:
            return ContenuProjet.objects.get(id=id)
        except ContenuProjet.DoesNotExist:
            return None
    
    def get(self,request,id,*args, **kwargs):
        contenu = self.get_contenu(id=id)
        if not contenu:
            return Response({"reponse":"Ce contenu n'existe pas!"})
        activite = ActiviteContenu.objects.filter(contenu=id)
        serializer = ActiviteContenuSerializer(activite,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        serializer = ActiviteContenuCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activite = serializer.save()
        return Response(ActiviteContenuSerializer(activite).data,status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class ActiviteDetailAPIView(APIView):

    def get_activite(self,id):
        try:
            return ActiviteContenu.objects.get(id=id)
        except ActiviteContenu.DoesNotExist:
            return None

    def get(self,request,id,*args, **kwargs):
        activite = self.get_activite(id=id)
        if not activite:
            return Response({"reponse":"Cette activite n'existe pas!"})
        activite = ActiviteContenu.objects.get(id=id)
        serializer = ActiviteContenuSerializer(activite)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,id,*args, **kwargs):
        activite = self.get_activite(id=id)
        if not activite:
            return Response({"reponse":"Cette activite  n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)
        serializer = ActiviteContenuCreateSerializer(instance=activite,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        activite = serializer.save()
        return Response(ActiviteContenuSerializer(activite).data, status=status.HTTP_201_CREATED)


    def delete(self,request,id,format=None):
        activite = self.get_activite(id=id)
        if not activite:
            return Response({"reponse":"Cette activite n'existe pas!"},status=status.HTTP_400_BAD_REQUEST)
        activite.delete()
        return Response({"reponse": "Suppression reussie!"},status=status.HTTP_200_OK)



    


    
    


    

    
    

    



    



















