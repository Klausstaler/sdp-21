# Generated by Django 3.1.5 on 2021-02-24 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0007_auto_20210223_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robot',
            name='status',
            field=models.BooleanField(blank=True, default=False, editable=False, null=True),
        ),
    ]
