# Generated by Django 4.0.2 on 2022-03-07 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='friendchatpage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromuser', models.CharField(max_length=25)),
                ('touser', models.CharField(max_length=25)),
                ('url', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(default='Active', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='friendmessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(default='12:56AM', max_length=25)),
                ('message', models.TextField()),
                ('touser', models.CharField(max_length=25)),
                ('fromuser', models.CharField(max_length=25)),
                ('url', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
