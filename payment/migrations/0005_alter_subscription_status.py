# Generated by Django 5.0.6 on 2024-06-12 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_payment_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='status',
            field=models.CharField(choices=[('active', 'Inactive'), ('inactive', 'Active'), ('expired', 'Expired')], default='inactive', max_length=20),
        ),
    ]
