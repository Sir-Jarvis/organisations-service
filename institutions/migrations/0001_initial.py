# Generated by Django 3.1.13 on 2021-12-21 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppelACandidature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debut', models.DateField()),
                ('fin', models.DateField()),
                ('typeStage', models.CharField(choices=[('Ouvrier', 'Ouvrier'), ('Maîtrise', 'Maîtrise'), ('PFE', 'PFE')], max_length=8)),
                ('nombre', models.IntegerField()),
                ('dureeStage', models.CharField(max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'AppelACandidature',
                'verbose_name_plural': 'AppelACandidatures',
            },
        ),
        migrations.CreateModel(
            name='Demande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debut', models.DateField()),
                ('fin', models.DateField()),
                ('user', models.IntegerField()),
                ('dateDemande', models.DateTimeField(auto_now_add=True)),
                ('fileUrl', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Demande',
                'verbose_name_plural': 'Demandes',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('localite', models.CharField(max_length=50)),
                ('numero_portable', models.CharField(max_length=50)),
                ('numero_fixe', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('domaine_activites', models.TextField()),
                ('logo', models.ImageField(blank=True, default='null', upload_to='logos')),
            ],
            options={
                'verbose_name': 'Institution',
                'verbose_name_plural': 'Institutions',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SousDemande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeStage', models.CharField(choices=[('Ouvrier', 'Ouvrier'), ('Maîtrise', 'Maîtrise'), ('PFE', 'PFE')], max_length=8)),
                ('niveau', models.CharField(choices=[('TC1', 'TC1'), ('TC2', 'TC2'), ('DIC1', 'DIC1'), ('DIC2', 'DIC2'), ('DIC3', 'DIC3')], max_length=4)),
                ('duree', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'SousDemandes',
                'verbose_name_plural': 'SousDemandes',
            },
        ),
        migrations.CreateModel(
            name='TypeOrganisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'TypeOrganisation',
                'verbose_name_plural': 'TypeOrganisations',
            },
        ),
        migrations.CreateModel(
            name='UrlsInstitutionDemande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileUrl', models.URLField()),
                ('demande', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='institutions.demande')),
                ('institution', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='institutions.institution')),
            ],
            options={
                'verbose_name': 'UrlsInstitutionDemande',
                'verbose_name_plural': 'UrlsInstitutionDemandes',
            },
        ),
        migrations.CreateModel(
            name='Offre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debut', models.DateField()),
                ('fin', models.DateField()),
                ('nombre', models.IntegerField()),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('institution', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='institutions.institution')),
                ('sousDemande', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offres', to='institutions.sousdemande')),
            ],
            options={
                'verbose_name': 'Offre',
                'verbose_name_plural': 'Offres',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='institution',
            name='typeOrganisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organisation', to='institutions.typeorganisation'),
        ),
        migrations.AddField(
            model_name='demande',
            name='institutions',
            field=models.ManyToManyField(blank=True, to='institutions.Institution'),
        ),
        migrations.AddField(
            model_name='demande',
            name='sousDemandes',
            field=models.ManyToManyField(to='institutions.SousDemande'),
        ),
        migrations.CreateModel(
            name='ContenuProjet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projetName', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('appelACandidature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contenu', to='institutions.appelacandidature')),
                ('offre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contenu', to='institutions.offre')),
            ],
            options={
                'verbose_name': 'ContenuProjet',
                'verbose_name_plural': 'ContenuProjets',
            },
        ),
        migrations.AddField(
            model_name='appelacandidature',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appelACandidature', to='institutions.institution'),
        ),
        migrations.CreateModel(
            name='ActiviteContenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomActivite', models.CharField(max_length=50)),
                ('contenu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activite', to='institutions.contenuprojet')),
            ],
            options={
                'verbose_name': 'ActiviteContenu',
                'verbose_name_plural': 'ActiviteContenus',
            },
        ),
    ]
