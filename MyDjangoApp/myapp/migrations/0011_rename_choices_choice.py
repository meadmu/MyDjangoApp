# Generated by Django 4.2.5 on 2024-01-03 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_choices'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Choices',
            new_name='Choice',
        ),
    ]