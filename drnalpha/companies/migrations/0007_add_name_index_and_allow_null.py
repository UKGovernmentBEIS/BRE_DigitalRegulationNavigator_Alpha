# Generated by Django 3.1.7 on 2021-03-12 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_split_number_of_employees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
    ]
