# Generated by Django 2.2.1 on 2020-06-19 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_auto_20200617_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectionpoint',
            name='memo',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='memo'),
        ),
    ]