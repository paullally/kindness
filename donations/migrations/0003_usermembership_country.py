# Generated by Django 4.0.1 on 2022-02-07 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0002_remove_membership_description_one_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermembership',
            name='country',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
