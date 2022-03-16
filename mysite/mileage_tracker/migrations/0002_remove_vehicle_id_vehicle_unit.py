# Generated by Django 4.0.3 on 2022-03-16 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mileage_tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='id',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='unit',
            field=models.CharField(default='filler', max_length=8, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]