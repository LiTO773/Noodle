from sqlite3 import Connection


def get_config_sections(conn: Connection, id: int) -> list:
    # Get the sections
    c = conn.cursor()
    c.execute("SELECT * FROM sections WHERE course_id = ?", (id,))

    rows = c.fetchall()
    c.close()

    return rows
