import psycopg2


class TestPostgres:
    """Context for PostgreSQL database testing"""

    def __init__(self, db_name, host="localhost", port="5432"):
        self._db_name = db_name
        self.host = host
        self.port = port
        self.url = f"postgresql://postgres:postgres@{host}/{db_name}"

    def connect(self):
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host=self.host,
            port=self.port,
        )
        conn.autocommit = True

        self._conn = conn

    def disconnect(self):
        self._conn.close()

    def create(self):
        self._conn.cursor().execute(f'CREATE DATABASE "{self._db_name}"')

    def recreate(self):
        self.drop()
        self.create()

    def drop(self, force=True):
        drop_query = f'DROP DATABASE IF EXISTS "{self._db_name}"'

        self._conn.cursor().execute(
            f"{drop_query} WITH (FORCE)" if force else drop_query
        )

    def __enter__(self):
        self.connect()
        self.recreate()

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.drop()
        self.disconnect()

        return True
