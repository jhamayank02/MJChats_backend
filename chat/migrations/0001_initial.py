# Generated by Django 3.2.9 on 2022-02-07 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_code', models.TextField()),
                ('room_creator', models.TextField()),
                ('room_pass', models.TextField()),
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
