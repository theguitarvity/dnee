# Generated by Django 2.1 on 2018-10-05 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_noticia'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
