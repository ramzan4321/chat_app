# Generated by Django 4.2.2 on 2023-06-28 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatmessages_media_chatmessages_media_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessages',
            name='group_name',
            field=models.CharField(default='Not provided', max_length=200),
        ),
    ]
