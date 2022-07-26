# Generated by Django 2.2.1 on 2020-07-13 18:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0007_taskamount'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskamount',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 13, 18, 12, 8, 599564, tzinfo=utc), null=True, verbose_name='timestamp'),
        ),
        migrations.AddField(
            model_name='taskreport',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 13, 18, 12, 8, 598988, tzinfo=utc), null=True, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='collectionpoint',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='collection_points', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='taskreport',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='reports', verbose_name='image'),
        ),
    ]
