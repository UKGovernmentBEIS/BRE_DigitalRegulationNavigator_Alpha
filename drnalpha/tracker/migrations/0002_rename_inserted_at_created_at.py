# Generated by Django 3.0.12 on 2021-02-09 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='step',
            old_name='inserted_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='inserted_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='tracker',
            old_name='inserted_at',
            new_name='created_at',
        ),
    ]
