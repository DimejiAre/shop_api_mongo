# from common.database import Database
import uuid
from common.sql_database import *


class User(object):
    def __init__(self, username, password, admin=False, _id=None):
        self.username = str(username)
        self.password = str(password)
        self.admin = admin
        if _id is None:
            self._id = uuid.uuid4().hex
        else:
            self._id = _id

    def json_data(self):
        return {
            "username": self.username,
            "password": self.password,
            "admin": self.admin,
            "_id": self._id
        }

    # mongo function to save to database
    # def save_to_mongo(self):
    #     return Database.insert(collection="user", data=self.json_data())

    def save_to_mongo(self):
        create_user_table()
        insert_user(user_id=self._id, username=self.username, password=self.password, admin=self.admin)

    # mongo function to get users
    # @staticmethod
    # def get_users():
    #     return [user for user in Database.find(collection="user")]

    @staticmethod
    def get_users():
        rows = view("user")
        row_list = []
        for row in rows:
            row_list.append({"user_id": row[1],
                             "username": row[2],
                             "password": row[3],
                             "admin": row[4]})
        return row_list

    # mongo function to get user by name
    # @staticmethod
    # def get_user_by_username(name):
    #     return Database.find_one(collection="user", query={"username": name})

    @staticmethod
    def get_user_by_username(name):
        rows = view_one_name(name)
        row = rows[0]
        return {"item_id": row[1],
                "username": row[2],
                "password": row[3],
                "admin": row[4]}

    # mongo function to get user by id
    # @staticmethod
    # def get_user_by_id(id):
    #     return Database.find_one(collection="user", query={"_id": id})

    @staticmethod
    def get_user_by_id(id):
        rows = view_one("user", id)
        row = rows[0]
        return {"item_id": row[1],
                "username": row[2],
                "password": row[3],
                "admin": row[4]}

    # mongo function for getting userclass by username
    # @classmethod
    # def get_userclass_by_username(cls, name):
    #     response = Database.find_one(collection="user", query={"username": name})
    #     user = cls(**response)
    #     return user

    @classmethod
    def get_userclass_by_username(cls, name):
        rows = view_one_name(name)
        row = rows[0]
        user = User(_id=row[1], username=row[2], password=row[3], admin=row[4])
        return user

    # mongo function for getting user class_by_id
    # @classmethod
    # def get_userclass_by_id(cls, user_id):
    #     response = Database.find_one(collection="user", query={"_id": user_id})
    #     user = cls(**response)
    #     return user

    @classmethod
    def get_userclass_by_id(cls, user_id):
        rows = view_one("user", user_id)
        row = rows[0]
        user = User(_id=row[1], username=row[2], password=row[3], admin=row[4])
        return user

    # mongo function for  update_user_by_name
    # @staticmethod
    # def update_user_by_name(name, data):
    #     Database.update_one(collection="user", query={"username": name}, data=data)

    @staticmethod
    def update_user_by_name(name, data):
        print("Method has not been configured {} {}", format(name, data))

    # mongo function for updating user by id
    # @staticmethod
    # def update_user_by_id(id, data):
    #     Database.update_one(collection="user", query={"_id": id}, data=data)

    @staticmethod
    def update_user_by_id(id, data):
        username = password = admin = None

        if "username" in data:
            username = data["username"]
        if "password" in data:
            password = data["password"]
        if "admin" in data:
            admin = data["admin"]

        data = view_one("user", id)
        data = data[0]
        if username is None:
            username = data[2]
        if password is None:
            password = data[3]
        if admin is None:
            admin = data[4]

        update_user(id, username, password, admin)

    # mongo function for deleting user by id
    # @staticmethod
    # def delete_user_by_id(id):
    #     Database.delete_one(collection="user", query={"_id": id})

    @staticmethod
    def delete_user_by_id(id):
        delete_data(table="user", id=id)