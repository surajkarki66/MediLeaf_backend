# Generated by Django 4.2.1 on 2023-05-30 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0009_alter_plant_other_resources_links_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantspecies',
            name='genus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='species_set', to='plant.plantgenus'),
        ),
    ]
