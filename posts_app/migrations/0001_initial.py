# Generated by Django 4.2.3 on 2023-07-28 01:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('message_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(upload_to='files')),
            ],
        ),
        migrations.CreateModel(
            name='PostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='gallery')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ManyToManyField(blank=True, related_name='categories', to='posts_app.categorymodel')),
                ('disslikes', models.ManyToManyField(related_name='disslikes', to=settings.AUTH_USER_MODEL)),
                ('files', models.ManyToManyField(to='posts_app.filemodel')),
                ('likes', models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('messages', models.ManyToManyField(blank=True, related_name='messages', to='message_app.messagesmodel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
