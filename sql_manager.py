import sqlite3
import threading
from typing import Tuple, Any, List


class SqlManager:
    def __init__(self, db):
        self.mutex = threading.Lock()
        self.db = db

    def execute_sql_query(self, query, parameters=None) -> List[Tuple[Any, ...]]:
        try:
            self.mutex.acquire()
            con = sqlite3.connect(self.db)
            cur = con.cursor()
            if parameters:
                cur.execute(query, parameters)
            else:
                cur.execute(query)
            result = cur.fetchall()
            con.commit()
            con.close()
            return result
        except Exception as e:  # noqa
            return []
        finally:
            self.mutex.release()
