# Generated by Django 5.1.4 on 2025-04-17 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr_app', '0017_alter_attendance_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='salary',
        ),
    ]
