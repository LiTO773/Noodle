from sqlite3 import Connection


def get_config_urls(conn: Connection, id: int, is_section: bool) -> list:
    # Get the urls
    c = conn.cursor()
    c.execute("SELECT * FROM urls WHERE section_id = ?", (id,))

    if is_section:
        c.execute("SELECT * FROM urls WHERE section_id = ?", (id,))
    else:
        c.execute("SELECT * FROM urls WHERE folder_id = ?", (id,))

    rows = c.fetchall()
    c.close()

    return rows
