# Generated by Django 5.1.5 on 2025-02-09 08:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_participants'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='confirm_participants',
            field=models.ManyToManyField(related_name='confirmed_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
