# Generated by Django 2.2.1 on 2020-06-17 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import location_field.models.plain


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'BaseRoute',
                'verbose_name_plural': 'BaseRoutes',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='name')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Garbage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='name')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Garbage',
                'verbose_name_plural': 'Garbages',
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', location_field.models.plain.PlainLocationField(max_length=63, null=True, verbose_name='location')),
                ('registration_number', models.CharField(max_length=15, unique=True, verbose_name='registration_number')),
                ('model', models.CharField(blank=True, max_length=20, verbose_name='model')),
            ],
            options={
                'verbose_name': 'Vehicle',
                'verbose_name_plural': 'Vehicles',
            },
        ),
        migrations.CreateModel(
            name='TaskRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='name')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_route', to='master.Customer', verbose_name='customer')),
                ('garbage', models.ManyToManyField(blank=True, related_name='task_route', to='master.Garbage', verbose_name='garbage')),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_route', to='master.Vehicle', verbose_name='vehicle')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
        ),
        migrations.CreateModel(
            name='TaskCollectionPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', location_field.models.plain.PlainLocationField(max_length=63, verbose_name='location')),
                ('name', models.CharField(max_length=20, verbose_name='name')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='address')),
                ('sequence', models.IntegerField(verbose_name='sequence')),
                ('image', models.FileField(blank=True, null=True, upload_to='', verbose_name='image')),
                ('route', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_collection_point', to='master.TaskRoute', verbose_name='route')),
            ],
            options={
                'verbose_name': 'TaskCollectionPoint',
                'verbose_name_plural': 'TaskCollectionPoints',
            },
        ),
        migrations.CreateModel(
            name='TaskCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=None, null=True, verbose_name='timestamp')),
                ('complete', models.BooleanField(default=False)),
                ('amount', models.IntegerField(default=0)),
                ('image', models.FileField(blank=True, null=True, upload_to='', verbose_name='image')),
                ('available', models.BooleanField(default=False)),
                ('collection_point', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_collection', to='master.TaskCollectionPoint', verbose_name='collection_point')),
                ('garbage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='master.Garbage', verbose_name='garbage')),
                ('users', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='users')),
                ('vehicle', models.ForeignKey(null=True, on_delete=None, related_name='collection', to='master.Vehicle', verbose_name='vehicle')),
            ],
            options={
                'verbose_name': 'TaskCollection',
                'verbose_name_plural': 'TaskCollections',
            },
        ),
        migrations.CreateModel(
            name='CollectionPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', location_field.models.plain.PlainLocationField(max_length=63, verbose_name='location')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='name')),
                ('address', models.CharField(blank=True, max_length=100, verbose_name='address')),
                ('sequence', models.IntegerField(null=True, verbose_name='sequence')),
                ('image', models.FileField(blank=True, null=True, upload_to='', verbose_name='image')),
                ('route', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collection_point', to='master.BaseRoute', verbose_name='route')),
            ],
            options={
                'verbose_name': 'CollectionPoint',
                'verbose_name_plural': 'CollectionPoints',
            },
        ),
        migrations.AddField(
            model_name='baseroute',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='route', to='master.Customer', verbose_name='customer'),
        ),
        migrations.AddField(
            model_name='baseroute',
            name='garbage',
            field=models.ManyToManyField(blank=True, related_name='route', to='master.Garbage', verbose_name='garbage'),
        ),
    ]
