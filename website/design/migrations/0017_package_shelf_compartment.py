# Generated by Django 3.1.5 on 2021-02-25 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0016_package_shelf'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='shelf_compartment',
            field=models.IntegerField(blank=True, null=True, verbose_name='Compartment'),
        ),
    ]
