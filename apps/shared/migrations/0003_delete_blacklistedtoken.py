# Generated by Django 4.2.11 on 2024-10-22 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0002_alter_blacklistedtoken_token'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BlacklistedToken',
        ),
    ]