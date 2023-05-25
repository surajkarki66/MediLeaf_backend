# Generated by Django 4.2.1 on 2023-05-24 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plant', '0005_alter_plantimage_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantimage',
            name='part',
            field=models.CharField(choices=[('flower', 'Flower'), ('leaf', 'Leaf'), ('fruit', 'Fruit'), ('bark', 'Bark'), ('other', 'Other')], max_length=7),
        ),
    ]
