from cassandra.cluster import Cluster
from cassandra.util import uuid_from_time
from cassandra.query import BatchStatement, ConsistencyLevel

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time

# Configuration
SCYLLA_HOST = "scylla"
KEYSPACE = "chat"
NUM_CHANNELS = 10_000  # Number of distinct channels
NUM_USERS = 1_000  # Number of distinct users
TOTAL_MESSAGES = 39_000_000  # Adjust as needed
BATCH_SIZE = 10000  # Messages per outer batch
SUB_BATCH_SIZE = 500  # Rows per Scylla batch
WORKERS = 18  # Number of parallel threads

#  Connect to Scylla
cluster = Cluster([SCYLLA_HOST], port=9042)
session = cluster.connect(KEYSPACE)
prepared_stmt = session.prepare(
    """
    INSERT INTO messages (channel_uid, message_id, sender_uid, content, created_at)
    VALUES (?, ?, ?, ?, ?)
"""
)


#  Generate one message row
def generate_message(i):
    created_at = datetime.utcnow()
    message_id = uuid_from_time(created_at)
    channel_uid = f"channel_{i % NUM_CHANNELS}"
    sender_uid = f"user_{i % NUM_USERS}"
    content = f"hello {i}"
    return (channel_uid, message_id, sender_uid, content, created_at)


#  Write a sub-batch of rows using Scylla BatchStatement
def write_batch(data_batch):
    batch = BatchStatement(consistency_level=ConsistencyLevel.ONE)
    for row in data_batch:
        batch.add(prepared_stmt, row)
    session.execute(batch)


#  Bulk insert loop
def bulk_insert():
    print(f"Starting insert of {TOTAL_MESSAGES:,} messages")
    start = time.time()

    for batch_start in range(0, TOTAL_MESSAGES, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, TOTAL_MESSAGES)
        data_batch = [generate_message(i) for i in range(batch_start, batch_end)]

        # Split into sub-batches
        sub_batches = [
            data_batch[i : i + SUB_BATCH_SIZE]
            for i in range(0, len(data_batch), SUB_BATCH_SIZE)
        ]

        # Run inserts in parallel
        with ThreadPoolExecutor(max_workers=WORKERS) as executor:
            executor.map(write_batch, sub_batches)

        if batch_start % 10_000 == 0:
            elapsed = time.time() - start
            print(
                f"Inserted {batch_end:,} / {TOTAL_MESSAGES:,} messages in {elapsed:.2f}s"
            )

    total_time = time.time() - start
    print(f"DONE. Inserted {TOTAL_MESSAGES:,} messages in {total_time:.2f} seconds")


#  entry point
if __name__ == "__main__":
    bulk_insert()
