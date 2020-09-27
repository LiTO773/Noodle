from sqlite3 import Connection


def get_config_files(conn: Connection, id: int, is_section: bool) -> list:
    # Get the files
    c = conn.cursor()

    if is_section:
        c.execute("SELECT * FROM files WHERE section_id = ?", (id,))
    else:
        c.execute("SELECT * FROM files WHERE folder_id = ?", (id,))

    rows = c.fetchall()
    c.close()

    return rows
