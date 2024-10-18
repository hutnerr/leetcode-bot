""" 
Helper module to work with SQlite3 databases.

Functions: 
    - connectDB(name: str) -> tuple: 
    - addRow(table: str, columns: tuple, values: tuple) -> bool:
    - updateRow(table: str, column: str, value: str, condition: str) -> bool:
    - removeRow(table: str, condition: str, params: tuple) -> bool:
    - getRow(table: str, condition: str, params: tuple) -> tuple:
    - getRowsWhere(table: str, condition: str, params: tuple) -> tuple:
    - getRows(table: str) -> tuple:
    - wipeDB(table: str) -> bool:
    - contains(table: str, condition: str, params: tuple) -> bool:
"""

import os
import sqlite3

FILEPATH = os.path.join("data", "databases")

def connectDB(name: str) -> tuple:
    """
    Helper method to connect to a database
    Args:
        name (str): The name of the database. In tools.consts.DatabaseTables
    Returns:
        tuple: The conn and cursor objects for the database
    """
    conn = sqlite3.connect(os.path.join(FILEPATH, f'{name}.db'))
    cursor = conn.cursor()
    return (conn, cursor)

def addRow(table: str, columns: tuple, values: tuple) -> bool:
    """
    Adds a row to a table in the database
    Args:
        table (str): The name of the table. Use tools.consts.DatabaseTables
        columns (tuple): The columns the table has. Use tools.consts.DatabaseFields
        values (tuple): A corresponding tuple of values to insert into the table
    Returns:
        bool: True if the row was added successfully, False if an error occurred
    """
    try:
        conn, cursor = connectDB(table)
        query = f"INSERT INTO {table} {columns} VALUES ?"
        cursor.execute(query, values)
        # cursor.execute(f"INSERT INTO {table} {columns} VALUES {values}")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def updateRow(table: str, column: str, value: str, condition: str) -> bool:
    """
    Updates a row in a table in the database
    Args:
        table (str): The name of the table. Use tools.consts.DatabaseTables
        column (str): The individual column to update. 
        value (str): The value to update the column to
        condition (str): The condition to update the row. e.g. "id = 12345"
    Returns:
        bool: True if the row was updated successfully, False if an error occurred
    """
    try:
        conn, cursor = connectDB(table)
        query = f"UPDATE {table} SET {column} = ? WHERE {condition}"
        cursor.execute(query, (value,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def removeRow(table: str, condition: str, params: tuple) -> bool:
    """
    Removes an individual row from a table in the database
    Args:
        table (str): The name of the table. Use tools.consts.DatabaseTables
        condition (str): The condition to remove the row. e.g. "id = ?"
        params (tuple): The parameters to pass to the condition. e.g. (12345,)
    Returns:
        bool: True if the row was removed successfully, False if an error occurred
    """
    try:
        conn, cursor = connectDB(table)
        query = f"DELETE FROM {table} WHERE {condition}"
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def getRow(table: str, condition: str, params: tuple) -> tuple:
    """
    Gets a single row from a table in the database. 
    Args:
        table (str): The name of the table. Use tools.consts.DatabaseTables
        condition (str): The condition to get the row. e.g. "id = ?"
        params (tuple): The parameters to pass to the condition. e.g. (12345,)
    Returns:
        tuple: The row from the table. None if failed 
    """
    try:
        conn, cursor = connectDB(table)
        query = f"SELECT * FROM {table} WHERE {condition}"
        cursor.execute(query, params)
        return cursor.fetchone()
    except Exception as e:
        print(e)
        return None

def getRowsWhere(table: str, condition: str, params: tuple) -> tuple:
    """
    Gets all of the rows using a condition
    Args:
        table (str): The name of the table. Use tools.consts.DatabaseTables
        condition (str): The condition to get the row. e.g. "id = ?"
        params (tuple): The parameters to pass to the condition. e.g. (12345,)
    Returns:
        tuple: The rows from the table . None if failed 
    """
    try:
        conn, cursor = connectDB(table)
        query = f"SELECT * FROM {table} WHERE {condition}"
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None

def getRows(table: str) -> tuple:
    """
    Gets all of the rows from a table
    Args:
        table (str): The name of the table. Use tools.consts.DatabaseTables
    Returns:
        tuple: All of the rows from the table. None if failed
    """
    try:
        conn, cursor = connectDB(table)
        cursor.execute(f"SELECT * FROM {table}")
        return cursor.fetchall()
    except Exception as e:
        print(e)
        return None
        
def wipeDB(table: str) -> bool:
    """
    Wipes the database of all rows
    Args:
        table (str): The name of the table. Use tools.consts.DatabaseTables
    Returns:
        bool: True if the database was wiped successfully, False if an error occurred
    """
    try:
        conn, cursor = connectDB(table)
        cursor.execute(f"DELETE FROM {table}")
        conn.commit()
        conn.close()
        return True        
    except Exception as e:
        print(e)
        return False
    
def contains(table: str, condition: str, params: tuple) -> bool:
    """
    Checks if a row exists within a table
    Args:
        table (str): The table to check. Use tools.consts.DatabaseTables
        condition (str): The condition to check. e.g. "id = ?"
        params (tuple): The values to pass to the condition. e.g. (12345,)
    Returns:
        bool: True if the row exists, False if it does not
    """
    conn, cursor = connectDB(table)
    query = f"SELECT * FROM {table} WHERE {condition}"
    cursor.execute(query, params)
    return cursor.fetchone() is not None