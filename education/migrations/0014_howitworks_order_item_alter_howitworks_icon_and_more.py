# Generated by Django 4.1.2 on 2023-05-14 06:31

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0013_rename_howitwork_howitworks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='howitworks',
            name='order_item',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='howitworks',
            name='icon',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='howitworkstranslation',
            name='content',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=500, verbose_name='content')),
        ),
    ]
