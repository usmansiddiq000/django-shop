# Generated by Django 2.2 on 2019-06-28 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='use_next_time',
        ),
        migrations.AddField(
            model_name='address',
            name='default_address',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='address',
            name='payment_method',
            field=models.CharField(max_length=10),
        ),
    ]
