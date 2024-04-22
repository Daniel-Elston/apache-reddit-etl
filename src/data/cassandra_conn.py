from __future__ import annotations

import uuid

from cassandra.cluster import Cluster


class CassandraManagement:
    """Manage Cassandra Operations"""

    def cassandra_conn():
        cluster = Cluster(['localhost/127.0.0.1:7000'])
        session = cluster.connect()
        return session

    def create_keyspace(session):
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS my_keyspace
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
            """)

    def create_table(session):
        session.execute("""
            CREATE TABLE IF NOT EXISTS my_keyspace.my_table (
                id UUID PRIMARY KEY,
                timestamp TIMESTAMP,
                comment TEXT)
            """)

    def insert_data(session):
        insert_statement = session.prepare("""
            INSERT INTO my_keyspace.my_table (id, timestamp, comment)
            VALUES (?, ?)
            """)
        session.execute(insert_statement, (uuid.uuid4(), 'reddit data'))

    def main(self):
        session = self.cassandra_conn()
        self.create_keyspace(session)
        self.create_table(session)
        self.insert_data(session)
