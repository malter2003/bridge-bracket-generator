# Generated by Django 4.2.7 on 2023-11-27 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bracket_app', '0002_tournament_creator_alter_tournament_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='is_active',
        ),
        migrations.AddField(
            model_name='tournament',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
