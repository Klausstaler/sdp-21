# Generated by Django 3.1.5 on 2021-03-01 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0018_hidden_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package', to='design.hidden_package'),
        ),
    ]
