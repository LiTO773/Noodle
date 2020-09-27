from sqlite3 import Connection


def update_config_userid(conn: Connection, id: int, userid: int):
    """ Changes the persisted userid of a certain config """
    c = conn.cursor()
    c.execute("UPDATE configs SET userid = ? WHERE id = ?", (userid, id))
    conn.commit()
    c.close()