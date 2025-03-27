import psycopg

QUERIES_PATH = "queries/"
class DBManager:
    def __init__(self, dbname:str, user: str, password: str, host: str, port: int):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = self.connect()
    def connect(self) -> psycopg.Connection:
        self.conn = psycopg.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return self.conn

    def close(self):
        self.conn.close()

    def execute(self, query:str):
        with self.conn.cursor() as cursor:
            cursor.execute(query)

    def execute_file(self, filename: str):
        self.execute(open(f'./db/queries/{filename}').read())

    def load_init_data(self):
        self.execute_file('init_data.sql')

    def get_images(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM images")
            return cursor.fetchall()