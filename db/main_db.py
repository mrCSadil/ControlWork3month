import sqlite3
from db import queries

db = sqlite3.connect('db/products.sqlite3')
cursor = db.cursor()

async def DataBase_create():
    if db:
        print('Database already exists')
    cursor.execute(queries.CREATE_TABLE_products)
    cursor.execute(queries.CREATE_TABLE_client)

async def sql_insert_products(name, category, size, price, product_id , photo):
    cursor.execute(queries.INSERT_products_QUERY(
        name, category, size, price, product_id, photo
    ))
    db.commit()

def sql_get_all_products():
    cursor.execute("SELECT name, category, size, price, product_id , photo from products")
    return cursor.fetchall()

def sql_get_all_clients():
    cursor.execute("SELECT product_id, size, quantity, number, photo FROM clients")
    return cursor.fetchone()

async def sql_insert_client(product_id, size, quantity, number):
    cursor.execute(queries.INSERT_products_QUERY(
        product_id, size, quantity, number
    ))
    db.commit()