# Generated by Django 3.1.7 on 2021-03-22 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regulations', '0014_add_categories_m2m'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='jurisdiction',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='regulation',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='regulator',
            name='name',
            field=models.CharField(db_index=True, max_length=50, verbose_name='Short name'),
        ),
    ]
