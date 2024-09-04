import sqlite3
import uuid
from pathlib import Path

from sql_manager import SqlManager

CLIENT_1_UUID = uuid.uuid4().bytes.hex()
CLIENT_1_NAME = "Bob"

CLIENT_2_UUID = uuid.uuid4().bytes.hex()
CLIENT_2_NAME = "Alice"

MESSAGE_1_UUID = uuid.uuid4().bytes.hex()
MESSAGE_2_UUID = uuid.uuid4().bytes.hex()


def __add_example_tables(sql_manager: SqlManager) -> None:
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


def __insert_example_data_to_tables(sql_manager: SqlManager) -> None:
    sql_manager.insert(table_name="clients", values=[CLIENT_1_UUID, CLIENT_1_NAME])
    sql_manager.insert(table_name="clients", values=[CLIENT_2_UUID, CLIENT_2_NAME])
    sql_manager.insert(table_name="messages", values=[MESSAGE_1_UUID, CLIENT_1_UUID, CLIENT_2_UUID, "Hello Alice!"])
    sql_manager.insert(table_name="messages", values=[MESSAGE_2_UUID, CLIENT_2_UUID, CLIENT_1_UUID, "Hello Bob!"])


def main() -> None:
    EXAMPLE_DB_PATH = Path("server.db")
    open(EXAMPLE_DB_PATH, 'a').close()

    sql_manager = SqlManager(EXAMPLE_DB_PATH)

    __add_example_tables(sql_manager)
    __insert_example_data_to_tables(sql_manager)

    print("Select all clients:")
    print(f"{sql_manager.select(select='*', from_='clients')}\n")

    print("Select content of MESSAGE_1:")
    print(f'{sql_manager.select(select="Content", from_="messages", ID=MESSAGE_1_UUID)}\n')

    sql_manager.update('messages', {'Content': 'Edited message content'}, ID=MESSAGE_1_UUID)

    print("Select content of MESSAGE_1 after it was edited:")
    print(f'{sql_manager.select(select="Content", from_="messages", ID=MESSAGE_1_UUID)}\n')

    print("Select all messages:")
    print(f"{sql_manager.select(select='*', from_='messages')}\n")

    sql_manager.delete(from_="messages", ID=MESSAGE_1_UUID)
    print("Select all messages after deleted MESSAGE_1:")
    print(f'{sql_manager.select(select="*", from_="messages")}\n')

    try:
        sql_manager.drop_table('imaginary_table', throw_if_not_exists=True)
    except sqlite3.OperationalError as e:
        print(f'Caught an expected exception: "{e}"')
    sql_manager.drop_table('imaginary_table', throw_if_not_exists=False)
    sql_manager.drop_table("messages")
    sql_manager.drop_table("clients")


if __name__ == '__main__':
    main()
