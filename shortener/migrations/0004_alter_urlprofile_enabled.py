# Generated by Django 4.0 on 2021-12-21 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0003_auto_20190528_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlprofile',
            name='enabled',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
