# Generated by Django 5.1.3 on 2024-11-29 10:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_first', to=settings.AUTH_USER_MODEL, verbose_name='İlk Kullanıcı')),
                ('second_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_second', to=settings.AUTH_USER_MODEL, verbose_name='İkinci Kullanıcı')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Mesaj İçeriği')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='src.room', verbose_name='Oda')),
            ],
        ),
    ]