# Generated by Django 3.2 on 2022-06-20 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0020_auto_20211128_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskroute',
            name='base_route',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_route', to='master.baseroute', verbose_name='base_route'),
        ),
        migrations.AlterField(
            model_name='taskamount',
            name='deal_type',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Deal Type'),
        ),
        migrations.AlterField(
            model_name='taskamount',
            name='work_type',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Work Type'),
        ),
    ]
