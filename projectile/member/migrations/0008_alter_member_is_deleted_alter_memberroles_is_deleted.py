# Generated by Django 5.2.1 on 2025-06-20 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0007_remove_member_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, help_text='Soft delete flag, not actually deleted from the database.'),
        ),
        migrations.AlterField(
            model_name='memberroles',
            name='is_deleted',
            field=models.BooleanField(db_index=True, default=False, help_text='Soft delete flag, not actually deleted from the database.'),
        ),
    ]
