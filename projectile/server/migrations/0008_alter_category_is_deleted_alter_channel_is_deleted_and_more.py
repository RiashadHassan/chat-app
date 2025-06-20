# Generated by Django 5.2.1 on 2025-06-20 10:41

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_spectrum'),
        ('server', '0007_remove_invite_channel_remove_invite_channel_uid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, help_text='Soft delete flag, not actually deleted from the database.'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, help_text='Soft delete flag, not actually deleted from the database.'),
        ),
        migrations.AlterField(
            model_name='invite',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, help_text='Soft delete flag, not actually deleted from the database.'),
        ),
        migrations.AlterField(
            model_name='role',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, help_text='Soft delete flag, not actually deleted from the database.'),
        ),
        migrations.AlterField(
            model_name='rolepermission',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, help_text='Soft delete flag, not actually deleted from the database.'),
        ),
        migrations.AlterField(
            model_name='server',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, help_text='Soft delete flag, not actually deleted from the database.'),
        ),
        migrations.AlterField(
            model_name='server',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='owned_servers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='thread',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, help_text='Soft delete flag, not actually deleted from the database.'),
        ),
        migrations.CreateModel(
            name='ServerSpectrum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('is_deleted', models.BooleanField(db_index=True, default=False, help_text='Soft delete flag, not actually deleted from the database.')),
                ('spectrum_uid', models.CharField(blank=True, db_index=True, max_length=36)),
                ('server_uid', models.CharField(blank=True, db_index=True, max_length=36)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='server_links', to='server.server')),
                ('spectrum', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='spectrum_links', to='core.spectrum')),
            ],
            options={
                'ordering': ['-created_at'],
                'constraints': [models.UniqueConstraint(fields=('spectrum', 'server'), name='unique_server_spectrum')],
            },
        ),
    ]
