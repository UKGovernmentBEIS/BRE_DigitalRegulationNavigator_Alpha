# Generated by Django 3.0.12 on 2021-02-05 17:12

from django.db import migrations

import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('regulations', '0002_create_regulations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulation',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='regulator',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
