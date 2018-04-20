# Generated by Django 2.0.4 on 2018-04-20 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='user',
            name='verification_code',
            field=models.CharField(blank=True, db_index=True, max_length=6, null=True),
        ),
    ]