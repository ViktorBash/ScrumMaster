# Generated by Django 2.2.15 on 2020-09-05 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0006_auto_20200905_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='boards.Board'),
        ),
    ]
