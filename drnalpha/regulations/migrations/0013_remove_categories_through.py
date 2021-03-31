# Generated by Django 3.1.7 on 2021-03-03 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regulations', '0012_add_jurisdictions_m2m'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regulationcategory',
            name='content_object',
        ),
        migrations.RemoveField(
            model_name='regulationcategory',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='regulation',
            name='categories',
        ),
        migrations.DeleteModel(
            name='CategoryTag',
        ),
        migrations.DeleteModel(
            name='RegulationCategory',
        ),
    ]
