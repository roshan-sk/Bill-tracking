# Generated by Django 5.0.6 on 2024-07-06 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_rename_user_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='otp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
