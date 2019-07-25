# Generated by Django 2.2.2 on 2019-07-25 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_logodescription_logo_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='logodescription',
            name='x_coordinate',
            field=models.IntegerField(blank=True, default=100, null=True),
        ),
        migrations.AddField(
            model_name='logodescription',
            name='y_coordinate',
            field=models.IntegerField(blank=True, default=100, null=True),
        ),
        migrations.AlterField(
            model_name='logodescription',
            name='logo_size',
            field=models.IntegerField(blank=True, default=2, null=True),
        ),
        migrations.AlterField(
            model_name='patterndescription',
            name='pattern_size',
            field=models.IntegerField(blank=True, default=2, null=True),
        ),
    ]