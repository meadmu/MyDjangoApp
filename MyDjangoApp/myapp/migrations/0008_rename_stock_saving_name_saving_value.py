# Generated by Django 4.2.5 on 2023-12-27 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_debt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saving',
            old_name='stock',
            new_name='name',
        ),
        migrations.AddField(
            model_name='saving',
            name='value',
            field=models.FloatField(null=True),
        ),
    ]
