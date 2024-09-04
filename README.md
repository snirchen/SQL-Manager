<h1 align="center">SQL Manager</h1>
<h2 align="center">Background</h2>

This project provides a robust framework for securely managing SQL queries by wrapping them with thread-safe functions. Designed with security and performance in mind, it effectively prevents SQL injection attacks and ensures safe concurrent database access.

---
- [Key Features 🌟](#key-features-)
- [Why Use This Framework? 💡](#why-use-this-framework-)
- [Getting Started 🛠️](#getting-started-)
- [Examples 🔍](#examples-)
- [Contributions 👥](#contributions-)
- [License 📜](#license-)
---

## Key Features 🌟
* Thread Safety: Ensures that SQL queries are handled safely in multi-threaded environments, avoiding potential conflicts and data corruption.
* SQL Injection Prevention: Utilizes parameterized queries and other best practices to protect against SQL injection vulnerabilities.
* Enhanced Security: Implements secure coding techniques to safeguard your database interactions.
* Easy Integration: Seamlessly integrates with various SQL databases, providing a straightforward interface for executing queries.

## Why Use This Framework? 💡
* Security First: Safeguard your database from malicious attacks with built-in protection against SQL injection.
* Concurrent Access: Maintain data integrity and performance even with high levels of concurrent database access.
* Simplified Code: Write cleaner and more maintainable database code with thread-safe functions.

## Getting Started 🛠️
1. Ensure Python 3.x is installed on your system.
2. Clone the repository to your local machine.
3. Wrap your SQL queries with provided functions to ensure security and thread safety (see examples section).

## Examples 🔍
```python

CLIENT_1_UUID = uuid.uuid4().bytes.hex()
CLIENT_1_NAME = "Bob"

CLIENT_2_UUID = uuid.uuid4().bytes.hex()
CLIENT_2_NAME = "Alice"

MESSAGE_1_UUID = uuid.uuid4().bytes.hex()
MESSAGE_2_UUID = uuid.uuid4().bytes.hex()

sql_manager = SqlManager("server.db")  # Init

# Create tables
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

# Insert data into tables
sql_manager.insert(table_name="clients", values=[CLIENT_1_UUID, CLIENT_1_NAME])
sql_manager.insert(table_name="clients", values=[CLIENT_2_UUID, CLIENT_2_NAME])
sql_manager.insert(table_name="messages", values=[MESSAGE_1_UUID, CLIENT_1_UUID, CLIENT_2_UUID, "Hello Alice!"])
sql_manager.insert(table_name="messages", values=[MESSAGE_2_UUID, CLIENT_2_UUID, CLIENT_1_UUID, "Hello Bob!"])

# Select from tables
all_clients = sql_manager.select(select='*', from_='clients')
content_of_message_1 = sql_manager.select(select="Content", from_="messages", ID=MESSAGE_1_UUID

# Update data
sql_manager.update('messages', {'Content': 'Edited message content'}, ID=MESSAGE_1_UUID)

# Delete data
sql_manager.delete(from_="messages", ID=MESSAGE_1_UUID)

# Drop table
sql_manager.drop_table('imaginary_table', throw_if_not_exists=False)
```

## Contributions 👥
Contributions are welcome!
Feel free to fork this project, submit pull requests, or send me suggestions to improve the implementation.
Your feedback is highly appreciated!

## License 📜
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
