# Generated by Django 4.1.7 on 2023-03-18 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.CharField(max_length=40),
        ),
    ]