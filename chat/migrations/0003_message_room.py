# Generated by Django 2.2 on 2020-08-13 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.Room'),
        ),
    ]