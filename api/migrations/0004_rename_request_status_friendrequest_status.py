# Generated by Django 5.0.6 on 2024-06-21 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_friendrequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendrequest',
            old_name='request_status',
            new_name='status',
        ),
    ]