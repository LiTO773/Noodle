from sqlite3 import Connection


def get_config_courses(conn: Connection, id: int) -> list:
    # Get the courses
    c = conn.cursor()
    c.execute("SELECT * FROM courses WHERE moodle_id = ?", (id,))

    rows = c.fetchall()
    c.close()

    return rows
