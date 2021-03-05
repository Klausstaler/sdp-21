# Generated by Django 3.1.5 on 2021-02-04 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='node',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('x_coordinate', models.IntegerField(verbose_name='X')),
                ('y_coordinate', models.IntegerField(verbose_name='Y')),
                ('qr_code', models.ImageField(blank=True, upload_to='', verbose_name='Barcode')),
            ],
            options={
                'unique_together': {('x_coordinate', 'y_coordinate')},
            },
        ),
        migrations.CreateModel(
            name='shelf',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False, verbose_name='Name')),
                ('height', models.IntegerField(verbose_name='Height')),
                ('ending_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_node', to='design.node')),
                ('starting_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_node', to='design.node')),
            ],
            options={
                'verbose_name_plural': 'Shelves',
            },
        ),
        migrations.CreateModel(
            name='item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('code', models.IntegerField(verbose_name='id')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Picture')),
                ('shelf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shelf', to='design.shelf')),
            ],
        ),
    ]
