# Generated by Django 2.2.2 on 2019-07-25 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20190725_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='logodescription',
            name='logo_size',
            field=models.IntegerField(blank=True, default=200, null=True),
        ),
    ]
