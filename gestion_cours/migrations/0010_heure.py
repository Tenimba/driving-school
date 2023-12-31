# Generated by Django 4.2 on 2023-04-27 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cours', '0009_remove_cours_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Heure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heurePaye', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='heure', to='gestion_cours.eleve')),
            ],
            options={
                'verbose_name': 'Heure',
                'verbose_name_plural': 'Heures',
            },
        ),
    ]
