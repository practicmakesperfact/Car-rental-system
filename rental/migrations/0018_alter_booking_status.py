# Generated by Django 5.1.7 on 2025-04-03 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0017_booking_payment_status_alter_booking_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('pending Admin Approval', 'Pending Admin Approval'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=25),
        ),
    ]
