# Generated by Django 3.1.6 on 2021-02-19 01:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='update',
            name='next_update',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='segment',
            name='points',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='segment',
            name='post_end',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='segment',
            name='post_start',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
    ]
