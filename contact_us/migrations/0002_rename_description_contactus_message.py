# Generated by Django 4.2.2 on 2023-07-12 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact_us', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactus',
            old_name='description',
            new_name='message',
        ),
    ]
