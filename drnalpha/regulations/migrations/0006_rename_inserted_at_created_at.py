# Generated by Django 3.0.12 on 2021-02-09 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regulations', '0005_add_categories_to_regulations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='regulation',
            old_name='inserted_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='regulator',
            old_name='inserted_at',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='regulatorregulation',
            old_name='inserted_at',
            new_name='created_at',
        ),
    ]
