# Generated by Django 4.2 on 2023-05-02 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cours', '0020_rename_heuredispo_eleve_heuredispo'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspecteur',
            name='heuredispo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inspecteur',
            name='heureindispo',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
