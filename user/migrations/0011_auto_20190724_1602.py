# Generated by Django 2.2.3 on 2019-07-24 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20190723_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='social',
            field=models.ForeignKey(blank=True, max_length=20, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.SocialPlatform'),
        ),
    ]
