# Generated by Django 5.0.6 on 2024-07-29 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Name'),
        ),
    ]
