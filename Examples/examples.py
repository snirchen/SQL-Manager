from pathlib import Path

from sql_manager import SqlManager


def add_example_tables(sql_manager: SqlManager) -> None:
    sql_manager.create_table(table_name="clients",
                             fields={
                                 'ID': 'text NOT NULL PRIMARY KEY',
                                 'Name': 'varchar(255)'
                             },
                             throw_if_exists=False)

    sql_manager.create_table(table_name="messages",
                             fields={
                                 'ID': 'blob NOT NULL PRIMARY KEY',
                                 'ToClient': 'text NOT NULL',
                                 'FromClient': 'text NOT NULL',
                                 'Content': 'blob'
                             },
                             foreign_keys={
                                 'ToClient': 'clients(ID)',
                                 'FromClient': 'clients(ID)'
                             },
                             throw_if_exists=False)


def main() -> None:
    EXAMPLE_DB_PATH = Path("server.db")
    open(EXAMPLE_DB_PATH, 'a').close()

    sql_manager = SqlManager(EXAMPLE_DB_PATH)

    add_example_tables(sql_manager)


if __name__ == '__main__':
    main()
