# Generated by Django 3.0.8 on 2020-07-23 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0011_auto_20200723_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomparticipantmanager',
            name='room_seat',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='admin_portal.RoomParticipantAbstract'),
        ),
    ]