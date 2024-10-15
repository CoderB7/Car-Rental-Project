# Generated by Django 4.2.11 on 2024-10-15 11:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('origin', models.CharField(blank=True, max_length=64, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='brands/')),
                ('year', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('license_plate', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('transmission', models.CharField(choices=[('manual', 'MANUAL'), ('automatic', 'AUTOMATIC')], default='manual', max_length=25)),
                ('year', models.IntegerField()),
                ('color', models.CharField(max_length=20)),
                ('mileage', models.IntegerField()),
                ('doors', models.IntegerField()),
                ('seats', models.IntegerField()),
                ('fuel_type', models.CharField(choices=[('petrol', 'PETROL'), ('hybrid', 'HYBRID'), ('electric', 'ELECTRIC')], default='petrol', max_length=25)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='cars/')),
                ('type', models.CharField(choices=[('sedan', 'SEDAN'), ('coupe', 'COUPE'), ('suv', 'SUV'), ('sportscar', 'SPORTSCAR'), ('crossover', 'CROSSOVER'), ('pickup_truck', 'PICKUP_TRUCK'), ('limousine', 'LIMOUSINE')], default='sedan', max_length=25)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='car', to='cars.brand')),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
            },
        ),
    ]
