# Generated by Django 2.2.1 on 2020-06-03 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0006_auto_20200529_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcollectionpoint',
            name='name',
            field=models.CharField(max_length=20, verbose_name='name'),
        ),
    ]
