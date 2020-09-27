from sqlite3 import Connection


def get_config_folders(conn: Connection, id: int) -> list:
    # Get the sections
    c = conn.cursor()
    c.execute("SELECT * FROM folders WHERE section_id = ?", (id,))

    rows = c.fetchall()
    c.close()

    return rows
