from cassandra.cluster import Cluster

KEYSPACE = "chat"

def get_cluster():
    return Cluster(["scylla"], port=9042)

def setup_keyspace_and_table():
    cluster = get_cluster()
    session = cluster.connect()

    session.execute(f"""
    CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
    WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': 1 }}
    """)

    session.set_keyspace(KEYSPACE)

    session.execute(f"""
    CREATE TABLE IF NOT EXISTS messages (
        channel_uid text,
        message_id timeuuid,
        sender_uid text,
        content text,
        created_at timestamp,
        PRIMARY KEY (channel_uid, message_id)
    ) WITH CLUSTERING ORDER BY (message_id DESC)
    """)
    
    cluster.shutdown()
