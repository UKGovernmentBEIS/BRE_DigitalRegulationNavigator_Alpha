# Generated by Django 3.1.7 on 2021-03-09 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_add_number_of_employees'),
        ('tracker', '0008_change_tracker_user_to_not_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='tracker', to='companies.company'),
        ),
    ]
