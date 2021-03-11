# Generated by Django 3.1.5 on 2021-02-25 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0009_auto_20210224_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shelf',
            name='ending_node',
        ),
        migrations.RemoveField(
            model_name='shelf',
            name='starting_node',
        ),
        migrations.AddField(
            model_name='shelf',
            name='node',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Node', to='design.node'),
            preserve_default=False,
        ),
    ]