# Generated by Django 4.1.2 on 2023-05-20 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_photo_file_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.template', verbose_name='template'),
        ),
    ]
