# Generated by Django 5.2.1 on 2025-06-20 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_spectrum'),
        ('server', '0008_alter_category_is_deleted_alter_channel_is_deleted_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spectrum',
            options={'ordering': ['-server_count', 'name'], 'verbose_name_plural': 'Spectra'},
        ),
        migrations.AddField(
            model_name='spectrum',
            name='servers',
            field=models.ManyToManyField(related_name='spectra', through='server.ServerSpectrum', to='server.server'),
        ),
    ]
