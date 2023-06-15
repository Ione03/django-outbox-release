# Generated by Django 4.1.2 on 2023-05-08 12:07

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields
import parler.fields
import parler.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0002_alter_domain_unique'),
        ('education', '0009_slideshowtranslation_sub_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fasilities',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('view_count', models.PositiveIntegerField(default=0, editable=False)),
                ('slug', models.SlugField(blank=True, default='', max_length=255, unique=True)),
                ('status', models.SmallIntegerField(choices=[(1, 'Draft'), (2, 'Published')], default=2)),
                ('is_header_text', models.BooleanField(default=False)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='site')),
            ],
            options={
                'ordering': ['-updated_at'],
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='FasilitiesTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', django_cryptography.fields.encrypt(models.CharField(max_length=500, verbose_name='title'))),
                ('content', django_cryptography.fields.encrypt(ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='content'))),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='education.fasilities')),
            ],
            options={
                'verbose_name': 'fasilities Translation',
                'db_table': 'education_fasilities_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
