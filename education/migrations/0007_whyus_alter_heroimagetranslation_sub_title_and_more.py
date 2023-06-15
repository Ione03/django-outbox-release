# Generated by Django 4.1.2 on 2023-04-02 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('education', '0006_heroimage_heroimagetranslation'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhyUs',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('icon', models.CharField(max_length=100, verbose_name='icon')),
                ('status', models.SmallIntegerField(choices=[(1, 'Draft'), (2, 'Published')], default=2)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.site')),
            ],
            options={
                'verbose_name': 'why us',
                'verbose_name_plural': 'why us',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.AlterField(
            model_name='heroimagetranslation',
            name='sub_title',
            field=models.CharField(max_length=500, verbose_name='sub title'),
        ),
        migrations.CreateModel(
            name='WhyUsTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.CharField(max_length=500, verbose_name='description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='education.whyus')),
            ],
            options={
                'verbose_name': 'why us Translation',
                'db_table': 'education_whyus_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
