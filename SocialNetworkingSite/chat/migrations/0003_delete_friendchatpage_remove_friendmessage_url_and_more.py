# Generated by Django 4.0.2 on 2022-03-10 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_friendmessage_date_alter_friendmessage_url'),
    ]

    operations = [
        migrations.DeleteModel(
            name='friendchatpage',
        ),
        migrations.RemoveField(
            model_name='friendmessage',
            name='url',
        ),
        migrations.AlterField(
            model_name='friendmessage',
            name='date',
            field=models.CharField(default='02:11PM', max_length=25),
        ),
    ]