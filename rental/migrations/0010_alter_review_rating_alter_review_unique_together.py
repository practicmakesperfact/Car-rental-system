# Generated by Django 5.1.6 on 2025-03-08 08:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0009_alter_review_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('car', 'user')},
        ),
    ]
