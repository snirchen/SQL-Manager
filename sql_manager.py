import sqlite3
import threading
from pathlib import Path
from typing import Tuple, Any, List


class SqlManager:
    def __init__(self, db: Path):
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

    def create_table_if_not_exists(self, table_name: str, fields: dict = None,
                                   foreign_keys: dict = None) -> List[Tuple[Any, ...]]:
        fields_as_str = ''
        foreign_keys_as_str = ''

        if fields:
            for field in fields:
                fields_as_str += f'{field} {fields[field]}, '
            fields_as_str = fields_as_str[:-2]

        if foreign_keys:
            for foreign_key in foreign_keys:
                foreign_keys_as_str += f'FOREIGN KEY({foreign_key}) REFERENCES {foreign_keys[foreign_key]}, '
            foreign_keys_as_str = foreign_keys_as_str[:-2]

        table_data = fields_as_str if foreign_keys is None else f'{fields_as_str}, {foreign_keys_as_str}'

        return self.execute_sql_query(f'CREATE TABLE IF NOT EXISTS {table_name}({table_data})')

    def insert(self, table_name: str, values: list) -> List[Tuple[Any, ...]]:
        values_as_str_params = ""

        for _ in values:
            values_as_str_params += f'?, '
        values_as_str_params = values_as_str_params[:-2]

        return self.execute_sql_query(f'INSERT INTO {table_name} VALUES ({values_as_str_params})', values)

    def select(self, select: str, from_: str, **where_conditions: str) -> List[Tuple[Any, ...]]:
        if len(where_conditions):
            where_ = 'WHERE '
            for where_condition in where_conditions:
                where_ += f"{where_condition}=? AND "
            where_ = where_[:-5]
            return self.execute_sql_query(f'SELECT {select} FROM {from_} {where_}', list(where_conditions.values()))

        return self.execute_sql_query(f'SELECT {select} FROM {from_}')

    def delete(self, from_: str, **where_conditions: str) -> List[Tuple[Any, ...]]:
        if len(where_conditions):
            where_ = 'WHERE '
            for where_condition in where_conditions:
                where_ += f"{where_condition}=? AND "
            where_ = where_[:-5]
            return self.execute_sql_query(f'DELETE FROM {from_} {where_}', list(where_conditions.values()))

        return self.execute_sql_query(f'DELETE FROM {from_}')
