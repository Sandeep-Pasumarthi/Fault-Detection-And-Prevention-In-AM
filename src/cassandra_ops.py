from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import BatchStatement


class CassandraDBManagement:

    def __init__(self, bundle_path, client_id, client_secret):
        cloud_config = {"secure_connect_bundle": bundle_path}
        auth_provider = PlainTextAuthProvider(client_id, client_secret)
        self.cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        self.session = self.cluster.connect()

    def is_connected(self):
        if self.session.session_id:
            return True
        return False

    def execute_query(self, keyspace, query):
        self.session.execute(f"USE {keyspace};")
        result = self.session.execute(query).all()
        return result

    def create_table(self, keyspace, table_name, column_names, data_types, primary_keys=None):
        query = f"CREATE TABLE {table_name} ("
        table_query = []
        for i, j in zip(column_names, data_types):
            per_table = i+" "+j
            table_query.append(per_table)

        query += ', '.join(table_query)
        if primary_keys:
            primary_key_query = ", ".join(primary_keys)
            query += ", PRIMARY KEY "
            query += f"({primary_key_query})"

        query += ');'
        return self.execute_query(keyspace, query)

    def insert_values(self, keyspace, table_name, values):
        column_names, length = self.get_columns(keyspace, table_name)
        column_names = ', '.join(column_names)
        values_string = ', '.join(['%s']*length)
        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({values_string});"
        batch = BatchStatement()
        for value in values:
            batch.add(query, value)

        return self.execute_query(keyspace, batch)

    def get_columns(self, keyspace, table_name):
        query = f"select column_name from system_schema.columns where keyspace_name = '{keyspace}' and " \
                f"table_name = '{table_name}' ALLOW FILTERING;"
        result = self.execute_query(keyspace, query)
        columns = []
        length = 0
        for i in result:
            columns.append(i.column_name)
            length += 1

        return columns, length

    def get_values(self, keyspace, table_name):
        query = f"SELECT * FROM {table_name};"
        result = self.execute_query(keyspace, query)
        values = [i[:] for i in result]

        return values
