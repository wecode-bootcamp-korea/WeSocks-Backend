# Generated by Django 2.2.2 on 2019-07-16 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20190716_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogoType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'logo_type',
            },
        ),
        migrations.CreateModel(
            name='PatternType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'pattern_type',
            },
        ),
        migrations.RemoveField(
            model_name='logodescription',
            name='title',
        ),
        migrations.RemoveField(
            model_name='patterndescription',
            name='title',
        ),
        migrations.AddField(
            model_name='logodescription',
            name='label',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='patterndescription',
            name='label',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='logodescription',
            name='detail_option',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]