import sqlite3
import threading
from pathlib import Path
from typing import Tuple, Any, List


class SqlManager:
    def __init__(self, db: Path):
        self.mutex = threading.Lock()
        self.db = db

    def __execute_sql_query(self, query, parameters=None) -> List[Tuple[Any, ...]]:
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
        finally:
            self.mutex.release()

    def create_table(self, table_name: str,
                     fields: dict = None,
                     foreign_keys: dict = None,
                     throw_if_exists: bool = True) -> None:
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

        query = f'CREATE TABLE {"" if throw_if_exists else "IF NOT EXISTS "}{table_name}({table_data})'
        self.__execute_sql_query(query)

    def insert(self, table_name: str, values: list) -> None:
        values_as_str_params = ""

        for _ in values:
            values_as_str_params += f'?, '
        values_as_str_params = values_as_str_params[:-2]

        self.__execute_sql_query(f'INSERT INTO {table_name} VALUES ({values_as_str_params})', values)

    def select(self, select: str, from_: str, **where_conditions: str) -> List[Tuple[Any, ...]]:
        if len(where_conditions):
            where_ = 'WHERE '
            for where_condition in where_conditions:
                where_ += f"{where_condition}=? AND "
            where_ = where_[:-5]
            return self.__execute_sql_query(f'SELECT {select} FROM {from_} {where_}', list(where_conditions.values()))

        return self.__execute_sql_query(f'SELECT {select} FROM {from_}')

    def delete(self, from_: str, **where_conditions: str) -> None:
        if len(where_conditions):
            where_ = 'WHERE '
            for where_condition in where_conditions:
                where_ += f"{where_condition}=? AND "
            where_ = where_[:-5]
            self.__execute_sql_query(f'DELETE FROM {from_} {where_}', list(where_conditions.values()))
        else:
            self.__execute_sql_query(f'DELETE FROM {from_}')

    def update(self, table_name: str, updated_rows: dict, **where_conditions: str) -> None:
        update_ = 'SET ' if len(updated_rows) else ''
        for key in updated_rows:
            update_ += f"{key}=?, "
        if len(update_):
            update_ = update_[:-2]

        if len(where_conditions):
            where_ = 'WHERE '
            for where_condition in where_conditions:
                where_ += f"{where_condition}=? AND "
            where_ = where_[:-5]
            self.__execute_sql_query(f'UPDATE {table_name} {update_} {where_}',
                                     list(updated_rows.values()) + list(where_conditions.values()))
        else:
            self.__execute_sql_query(f'UPDATE {table_name} {update_}',
                                     list(updated_rows.values()) + list(where_conditions.values()))

    def drop_table(self, table_name: str, throw_if_not_exists: bool = True) -> None:
        self.__execute_sql_query(f"DROP TABLE {'' if throw_if_not_exists else 'IF EXISTS '}{table_name};")
