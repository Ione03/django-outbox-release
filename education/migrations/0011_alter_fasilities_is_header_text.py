# Generated by Django 4.1.2 on 2023-05-08 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0010_fasilities_fasilitiestranslation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fasilities',
            name='is_header_text',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
