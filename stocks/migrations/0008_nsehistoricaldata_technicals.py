# Generated by Django 3.2 on 2021-06-21 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0007_auto_20210619_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='nsehistoricaldata',
            name='technicals',
            field=models.BooleanField(default=True),
        ),
    ]
