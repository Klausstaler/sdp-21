# Generated by Django 3.1.5 on 2021-02-04 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0004_auto_20210204_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='details',
            field=models.TextField(blank=True),
        ),
    ]
