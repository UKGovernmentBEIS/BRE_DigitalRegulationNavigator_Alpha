# Generated by Django 3.0.12 on 2021-02-09 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sic_codes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='code',
            old_name='inserted_at',
            new_name='created_at',
        ),
    ]
