# Generated by Django 3.2.5 on 2021-08-07 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='featured_image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]