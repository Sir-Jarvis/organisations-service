from django.db import models
from django.db.models.constraints import UniqueConstraint

class Departement(models.Model):
    nom_dept = models.CharField(max_length=300)


class AnneeScolaire(models.Model):
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True,null=True)
    alias = models.CharField(max_length=9,null=True)

    def __str__(self):
        return self.alias

    

class AnneeScolaireUser(models.Model):
    id = models.PositiveBigIntegerField( primary_key=True)
    user_id = models.PositiveBigIntegerField()
    annee_id = models.PositiveBigIntegerField()

    class Meta:
        db_table = 'AnneeUser'
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'annee_id'], name='user_annee_unique')
        ]

# class DepartmentUser(models.Model):
#     id = models.PositiveBigIntegerField( primary_key=True)
#     user_id = models.PositiveBigIntegerField()
#     department_id = models.PositiveBigIntegerField()

#     class Meta:
#         db_table = 'DepartmentUser'
#         constraints = [
#             models.UniqueConstraint(fields=['user_id', 'department_id'], name='user_department_unique')
#         ]


# class Product(models.Model):
#     title = models.CharField(max_length=200)
#     image = models.CharField(max_length=200)
   

# class ProductUser(models.Model):
#     id = models.PositiveBigIntegerField( primary_key=True)
#     user_id = models.PositiveBigIntegerField()
#     product_id = models.PositiveBigIntegerField()

#     class Meta:
#         db_table = 'ProductUser'
#         constraints = [
#             models.UniqueConstraint(fields=['user_id', 'product_id'], name='user_product_unique')
#         ]