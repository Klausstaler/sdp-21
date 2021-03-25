# Generated by Django 3.1.7 on 2021-03-25 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0031_auto_20210317_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='holding_package',
        ),
        migrations.AlterField(
            model_name='hidden_package',
            name='height',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hidden_package',
            name='length',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hidden_package',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hidden_package',
            name='width',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='height',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='length',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='width',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='robot',
            name='height',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='robot',
            name='length',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='robot',
            name='width',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='drop_zone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DropNode', to='design.node')),
            ],
        ),
    ]
