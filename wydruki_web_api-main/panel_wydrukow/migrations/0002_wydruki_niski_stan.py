# Generated by Django 4.2.21 on 2025-05-29 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel_wydrukow', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wydruki',
            name='niski_stan',
            field=models.IntegerField(default=1, help_text='Próg niskiego stanu dla tego produktu'),
        ),
    ]
