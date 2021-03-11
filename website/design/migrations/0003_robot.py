# Generated by Django 3.1.5 on 2021-02-04 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0002_auto_20210204_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='robot',
            fields=[
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('ip_address', models.GenericIPAddressField(primary_key=True, serialize=False, verbose_name='IP')),
                ('status', models.BooleanField(blank=True, default=None, null=True)),
            ],
        ),
    ]