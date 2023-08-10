""" Helper function to get the last AUTO_INCREMENT key from a database connection

TODO: move into class DriverMySQL
"""
from ALMAFE.database.DriverMySQL import DriverMySQL
from typing import Optional

QUERY = "SELECT LAST_INSERT_ID()"

def getLastInsertId(conn: DriverMySQL) -> Optional[int]:
    """ Helper function to get the last AUTO_INCREMENT key from a database connection

    Returns None on any error.
    """
    try:
        conn.execute(QUERY)
        row = conn.fetchone()
        if row:
            return row[0]
    except:
        pass
    return None
            