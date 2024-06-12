# Generated by Django 5.0.6 on 2024-06-11 13:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('1 month', '1 month'), ('2 months', '2 months'), ('3 months', '3 months')], max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('expiry', models.DateTimeField(default=django.utils.timezone.now)),
                ('price', models.DecimalField(choices=[(1000.0, '1 month'), (2000.0, '2 months'), (3000.0, '3 months')], decimal_places=2, default=1000.0, max_digits=10)),
                ('old_price', models.DecimalField(choices=[(1200.0, '1 month'), (2400.0, '2 months'), (3600.0, '3 months')], decimal_places=2, default=1200.0, max_digits=10)),
            ],
        ),
    ]
