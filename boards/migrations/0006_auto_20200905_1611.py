# Generated by Django 2.2.15 on 2020-09-05 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_auto_20200904_0804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(default='Title', max_length=100, unique=True),
        ),
    ]
