import enum
import psycopg2


class PgDatabase:
    class Tables(enum.Enum):
        names_woman = "names_woman"
        names_man = "names_man"

    def __init__(
        self,
        host: str,
        port: int | str,
        user: str,
        password: str,
        db_name: str,
    ):
        self.db_connect_params = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "dbname": db_name,
        }

    def is_name_in_table(self, table: Tables, name: str) -> bool:
        if not isinstance(table, self.Tables):
            raise ValueError("Некорретная таблица")
        with psycopg2.connect(**self.db_connect_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table.value} WHERE name = %s", (name,))
                return bool(cursor.fetchone())
