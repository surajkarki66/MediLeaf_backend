# Generated by Django 4.2.2 on 2023-07-12 15:45

from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=64, verbose_name='first name')),
                ('last_name', models.CharField(max_length=64, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('subject', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='subject')),
                ('description', django_ckeditor_5.fields.CKEditor5Field()),
            ],
            options={
                'verbose_name': 'ContactUs',
                'verbose_name_plural': 'ContactUs',
                'ordering': ('-id',),
            },
        ),
    ]
