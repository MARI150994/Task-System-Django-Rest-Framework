# Generated by Django 3.1 on 2022-04-17 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0002_auto_20220414_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(blank=True, db_index=True, max_length=30, null=True),
        ),
    ]
