from django.db import models


"""Toutes nos tables"""

class TypeOrganisation(models.Model):
    nom =  models.CharField(max_length=50)  

    class Meta:
        verbose_name = ("TypeOrganisation")
        verbose_name_plural = ("TypeOrganisations")

    def __str__(self):
        return self.nom



class Institution(models.Model):
    nom = models.CharField(max_length=50)
    localite = models.CharField(max_length=50)
    numero_portable = models.CharField(max_length=50)
    numero_fixe = models.CharField(max_length=50)
    description = models.TextField()
    domaine_activites = models.TextField()
    typeOrganisation = models.ForeignKey(TypeOrganisation, on_delete=models.SET_NULL,null=True,related_name="organisation")
    logo = models.ImageField(upload_to="logos",blank=True,default='null')

    def __str__(self):
        return self.nom

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'


class SousDemande(models.Model):
    typeStage = (
        ('Ouvrier','Ouvrier'),
        ('Maîtrise','Maîtrise'),
        ('PFE','PFE')
    )
    niveau = (
        ('TC1', 'TC1'),
        ('TC2','TC2'),
        ('DIC1','DIC1'),
        ('DIC2','DIC2'),
        ('DIC3','DIC3')
    )
    typeStage = models.CharField(choices=typeStage,max_length=8)
    niveau = models.CharField(choices=niveau, max_length=4)
    duree = models.CharField(max_length=50)
    #demande = models.ForeignKey(Demande,on_delete=models.CASCADE,related_name="sousDemandes")
    
    class Meta:
        verbose_name = ("SousDemandes")
        verbose_name_plural = ("SousDemandes")

    def __str__(self):
        return f"{str(self.typeStage)} {self.niveau} "


class Demande(models.Model):
    debut = models.DateField()
    fin = models.DateField()
    user = models.IntegerField()
    institutions = models.ManyToManyField(Institution,blank=True) 
    dateDemande = models.DateTimeField(auto_now_add=True)
    fileUrl = models.URLField(max_length=200,blank=True,null=True)
    sousDemandes = models.ManyToManyField(SousDemande,blank=False)

    def __str__(self):
        return f"{self.debut}-{self.fin}"

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Demande'
        verbose_name_plural = 'Demandes'

class UrlsInstitutionDemande(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL,null=True,related_name="files")
    demande = models.ForeignKey(Demande, on_delete=models.SET_NULL,null=True,related_name="files")
    fileUrl = models.URLField(max_length=200)


    class Meta:
        verbose_name = ("UrlsInstitutionDemande")
        verbose_name_plural = ("UrlsInstitutionDemandes")

    def __str__(self):
        return str(self.institution)





#réponse de l'institution à une sousdemande donnée
class Offre(models.Model):
    debut = models.DateField()
    fin = models.DateField()
    nombre = models.IntegerField()
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL,null=True)
    sousDemande = models.ForeignKey(SousDemande,on_delete=models.SET_NULL,null=True,related_name="offres")
    dateCreated = models.DateTimeField(auto_now_add=True)
    #fileUrl = models.URLField(max_length=200, blank=True)
    #etudiants = models.ManyToManyField(Etudiant, through='Candidature', related_name="etudiants")

    def __str__(self):
        return str(self.sousDemande)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Offre'
        verbose_name_plural = 'Offres'


class AppelACandidature(models.Model):
    typeStage = (
        ('Ouvrier','Ouvrier'),
        ('Maîtrise','Maîtrise'),
        ('PFE','PFE')
    )
    niveau = (
        ('TC1', 'TC1'),
        ('TC2','TC2'),
        ('DIC1','DIC1'),
        ('DIC2','DIC2'),
        ('DIC3','DIC3')
    )
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL,null=True,related_name="appelACandidature")
    debut = models.DateField()
    fin = models.DateField()
    typeStage = models.CharField(choices=typeStage, max_length=8)
    nombre = models.IntegerField()
    dureeStage = models.CharField(max_length=50,null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
   

    class Meta:
        verbose_name = ("AppelACandidature")
        verbose_name_plural = ("AppelACandidatures")

    def __str__(self):
        return str(self.institution)





"""StartContenu"""


class ContenuProjet(models.Model):
    projetName = models.CharField(max_length=50)
    description = models.TextField()
    appelACandidature = models.ForeignKey(AppelACandidature, on_delete=models.CASCADE,related_name="contenu",null=True,blank=True)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE,related_name="contenu",null=True,blank=True)

    class Meta:
        verbose_name = ("ContenuProjet")
        verbose_name_plural = ("ContenuProjets")

    def __str__(self):
        return self.projetName


class ActiviteContenu(models.Model):
    nomActivite = models.CharField(max_length=50)
    contenu = models.ForeignKey(ContenuProjet, on_delete=models.CASCADE,related_name="activite")

    class Meta:
        verbose_name = ("ActiviteContenu")
        verbose_name_plural = ("ActiviteContenus")

    def __str__(self):
        return self.nomActivite


"""EndContenu"""









   