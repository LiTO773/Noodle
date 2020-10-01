from sqlite3 import Connection


def read_configs(conn: Connection) -> list:
    c = conn.cursor()
    c.execute("SELECT * FROM configs")

    rows = c.fetchall()
    c.close()

    return rows
