# Generated by Django 4.1.3 on 2023-08-12 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitrator', '0004_storestatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storestatus',
            name='id',
        ),
        migrations.AlterField(
            model_name='storestatus',
            name='store_id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
