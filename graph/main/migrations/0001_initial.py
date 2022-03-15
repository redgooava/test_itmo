# Generated by Django 2.2 on 2022-03-12 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NodeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isValueNode', models.BooleanField(blank=True, null=True)),
                ('typeOfOperation', models.CharField(blank=True, max_length=255, null=True)),
                ('indexOfChild', models.IntegerField(blank=True, null=True)),
                ('value', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
