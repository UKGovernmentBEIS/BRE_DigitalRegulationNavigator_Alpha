# Generated by Django 3.1.6 on 2021-02-19 15:56

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('regulations', '0008_add_importance_to_regulations'),
    ]

    operations = [
        migrations.CreateModel(
            name='JurisdictionTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='regulation',
            name='jurisdiction',
        ),
        migrations.CreateModel(
            name='RegulationJurisdiction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='regulation_jurisductions', to='regulations.regulation')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regulation_jurisductions', to='regulations.jurisdictiontag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='regulation',
            name='jurisdictions',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of jurisdictions.', related_name='regulations', through='regulations.RegulationJurisdiction', to='regulations.JurisdictionTag', verbose_name='Jurisdictions'),
        ),
    ]
