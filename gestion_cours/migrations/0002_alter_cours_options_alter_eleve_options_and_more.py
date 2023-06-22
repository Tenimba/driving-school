# Generated by Django 4.2 on 2023-04-19 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cours', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cours',
            options={'verbose_name': 'Cours', 'verbose_name_plural': 'Cours'},
        ),
        migrations.AlterModelOptions(
            name='eleve',
            options={'verbose_name': 'Elève', 'verbose_name_plural': 'Elèves'},
        ),
        migrations.AlterModelOptions(
            name='inspecteur',
            options={'verbose_name': 'Inspecteur', 'verbose_name_plural': 'Inspecteurs'},
        ),
        migrations.AlterModelOptions(
            name='secretaire',
            options={'verbose_name': 'Secrétaire', 'verbose_name_plural': 'Secrétaires'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Utilisateur', 'verbose_name_plural': 'Utilisateurs'},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='eleve',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='eleves', to='gestion_cours.user'),
        ),
        migrations.CreateModel(
            name='RendezVous',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('heure', models.TimeField()),
                ('eleve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rendezvous', to='gestion_cours.eleve')),
                ('inspecteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rendezvous', to='gestion_cours.inspecteur')),
            ],
            options={
                'verbose_name': 'Rendez-vous',
                'verbose_name_plural': 'Rendez-vous',
            },
        ),
    ]
