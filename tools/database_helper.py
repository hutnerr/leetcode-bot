import os
import sqlite3

FILEPATH = os.path.join("data", "databases")

def connectDB(name:str):
    conn = sqlite3.connect(os.path.join(FILEPATH, f'{name}.db'))
    cursor = conn.cursor()
    return conn, cursor

def addRow(table:str, columns:tuple, values:tuple):
    conn, cursor = connectDB(table)
    cursor.execute(f"INSERT INTO {table} {columns} VALUES {values}")
    conn.commit()
    conn.close()

def updateRow(table:str, column:str, value:str, condition:str):
    conn, cursor = connectDB(table)
    query = f"UPDATE {table} SET {column} = ? WHERE {condition}"
    cursor.execute(query, (value,))
    conn.commit()
    conn.close()

def removeRow(table: str, condition: str, params: tuple):
    conn, cursor = connectDB(table)
    query = f"DELETE FROM {table} WHERE {condition}"
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def getRow(table:str, condition:str, params:tuple):
    conn, cursor = connectDB(table)
    query = f"SELECT * FROM {table} WHERE {condition}"
    cursor.execute(query, params)
    return cursor.fetchone()

def getRowsWhere(table:str, condition:str, params:tuple):
    conn, cursor = connectDB(table)
    query = f"SELECT * FROM {table} WHERE {condition}"
    cursor.execute(query, params)
    return cursor.fetchall()

def getRows(table:str):
    conn, cursor = connectDB(table)
    cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()

def printRows(table:str):
    rows = getRows(table)
    for row in rows:
        print(row)
        
def wipeDB(table:str):
    conn, cursor = connectDB(table)
    cursor.execute(f"DELETE FROM {table}")
    conn.commit()
    conn.close()        
    
def contains(table:str, condition:str, params:tuple):
    conn, cursor = connectDB(table)
    query = f"SELECT * FROM {table} WHERE {condition}"
    cursor.execute(query, params)
    return cursor.fetchone() is not None