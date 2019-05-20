import sqlite3


def create_item_table():
    connection = sqlite3.connect("../common/shop.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS item (id INTEGER PRIMARY KEY, item_id TEXT, name TEXT,"
                   " description TEXT, type TEXT, quantity INTEGER, price REAL)")
    connection.commit()
    connection.close()


def create_user_table():
    connection = sqlite3.connect("../common/shop.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, user_id TEXT, username TEXT,"
                   " password TEXT, admin BOOLEAN)")
    connection.commit()
    connection.close()


def insert_item(item_id, name, description, type, quantity, price):
    connection = sqlite3.connect("../common/shop.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO item VALUES(NULL, ?, ?, ?, ?, ?, ?)", (item_id, name, description, type, quantity, price))
    connection.commit()
    connection.close()


def insert_user(user_id, username, password, admin):
    connection = sqlite3.connect("../common/shop.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO user VALUES(NULL, ?, ?, ?, ?)",
                   (user_id, username, password, admin))
    connection.commit()
    connection.close()


def view(table):
    connection = sqlite3.connect("../common/shop.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM {}".format(table))
    rows = cursor.fetchall()
    connection.close()
    return rows


def view_one(table, id):
    connection = sqlite3.connect("../common/shop.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM {} WHERE {} ='{}'".format(table, table + "_id", id))
    row = cursor.fetchall()
    connection.close()
    return row


def view_one_name(name):
    connection = sqlite3.connect("../common/shop.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE username=?", (name,))
    row = cursor.fetchall()
    connection.close()
    return row


def update_item(id, name, description, type, quantity, price):
    connection = sqlite3.connect("../common/shop.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE item SET name = ?, description = ?, type = ?, quantity= ?, price = ? WHERE item_id=?",
                   (name, description, type, quantity, price, id))
    connection.commit()
    connection.close()


def update_user(id, username, password, admin):
    connection = sqlite3.connect("../common/shop.db")
    cursor = connection.cursor()
    #cursor.execute("UPDATE {} SET username = '{}', password = '{}' WHERE user_id = '{}'".format("user", username, password, id))
    cursor.execute("UPDATE user SET username = ?, password = ?, admin = ? WHERE user_id = ?", (username, password, admin, id))
    connection.commit()
    connection.close()


def delete_data(table, id):
    connection = sqlite3.connect("../common/shop.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM {} WHERE {}='{}'".format(table, table + "_id", id))
    connection.commit()
    connection.close()