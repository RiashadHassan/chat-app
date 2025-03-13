# migrations/0001_initial.py
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry (
                id UUID NOT NULL,
                user_id UUID NOT NULL,
                action TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                PRIMARY KEY (id, timestamp)
            ) PARTITION BY RANGE (timestamp);
            """,
            reverse_sql="DROP TABLE partitioned_log_entry;",
        ),
        # Create partitions for each month from March 2024 to March 2025
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2024_03 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2024_03;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2024_04 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2024-04-01') TO ('2024-05-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2024_04;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2024_05 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2024-05-01') TO ('2024-06-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2024_05;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2024_06 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2024-06-01') TO ('2024-07-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2024_06;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2024_07 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2024-07-01') TO ('2024-08-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2024_07;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2024_08 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2024-08-01') TO ('2024-09-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2024_08;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2024_09 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2024-09-01') TO ('2024-10-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2024_09;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2024_10 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2024-10-01') TO ('2024-11-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2024_10;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2024_11 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2024-11-01') TO ('2024-12-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2024_11;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2024_12 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2024-12-01') TO ('2025-01-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2024_12;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2025_01 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2025_01;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2025_02 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2025_02;",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE partitioned_log_entry_2025_03 PARTITION OF partitioned_log_entry
            FOR VALUES FROM ('2025-03-01') TO ('2025-04-01');
            """,
            reverse_sql="DROP TABLE partitioned_log_entry_2025_03;",
        ),
    ]
