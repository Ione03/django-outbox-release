# Generated by Django 4.1.2 on 2023-04-09 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_modellistsetting_image_height_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='modellistsetting',
            unique_together={('model_list', 'template')},
        ),
    ]