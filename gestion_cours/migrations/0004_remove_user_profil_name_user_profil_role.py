# Generated by Django 4.2 on 2023-04-19 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cours', '0003_user_profil_alter_eleve_user_alter_inspecteur_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_profil',
            name='name',
        ),
        migrations.AddField(
            model_name='user_profil',
            name='role',
            field=models.CharField(default='eleve', max_length=50, null=True),
        ),
    ]
