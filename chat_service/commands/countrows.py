from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import time

cluster = Cluster(["scylla"], port=9042)
session = cluster.connect("chat")


def count_all_messages():
    print("Counting all messages...")
    start = time.time()

    query = SimpleStatement("SELECT message_id FROM messages", fetch_size=10_000)

    total = 0
    result = session.execute(query)

    for row in result:
        total += 1
        if total % 1_000_000 == 0:
            print(f"Counted {total:,} messages...")

    print(f"Total messages: {total:,}")
    print(f"Took {time.time() - start:.2f} seconds")


if __name__ == "__main__":
    count_all_messages()
