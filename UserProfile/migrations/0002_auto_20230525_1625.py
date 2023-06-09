# Generated by Django 3.2 on 2023-05-25 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('postal_code', models.CharField(blank=True, max_length=16, null=True, verbose_name='postal code')),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='province name')),
                ('latitude', models.CharField(max_length=16, verbose_name='latitude')),
                ('longitude', models.CharField(max_length=16, verbose_name='longitude')),
            ],
            options={
                'verbose_name': 'province',
                'verbose_name_plural': 'provinces',
                'db_table': 'province',
            },
        ),
        migrations.AlterField(
            model_name='car',
            name='plate_number',
            field=models.CharField(max_length=16, unique=True, verbose_name='plate number'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32, verbose_name='first name')),
                ('last_name', models.CharField(max_length=32, verbose_name='last name')),
                ('user_id', models.PositiveIntegerField(unique=True, verbose_name='user id')),
                ('phone_number', models.CharField(max_length=16, unique=True, verbose_name='phone number')),
                ('national_id', models.CharField(max_length=16, null=True, unique=True, verbose_name='national id')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='register date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='modification date')),
                ('address', models.ManyToManyField(related_name='user_addresses', to='UserProfile.Address')),
            ],
            options={
                'verbose_name': 'user_profile',
                'verbose_name_plural': 'user_profiles',
                'db_table': 'user_profile',
            },
        ),
        migrations.CreateModel(
            name='DriverProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32, verbose_name='first name')),
                ('last_name', models.CharField(max_length=32, verbose_name='last name')),
                ('user_id', models.PositiveIntegerField(unique=True, verbose_name='user id')),
                ('phone_number', models.CharField(max_length=16, unique=True, verbose_name='phone number')),
                ('national_id', models.CharField(max_length=16, unique=True, verbose_name='national id')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='is confirmed')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='register date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='modification date')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='UserProfile.address')),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='driver', to='UserProfile.car')),
            ],
            options={
                'verbose_name': 'driver_profile',
                'verbose_name_plural': 'driver_profiles',
                'db_table': 'driver_profile',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='city name')),
                ('latitude', models.CharField(max_length=16, verbose_name='latitude')),
                ('longitude', models.CharField(max_length=16, verbose_name='longitude')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cities', to='UserProfile.province')),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
                'db_table': 'city',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='UserProfile.city'),
        ),
    ]
