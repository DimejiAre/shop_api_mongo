# from common.database import Database
from common.sql_database import *
import uuid


class Item(object):

    def __init__(self, name, description, type, price, quantity=1, id=None):
        self.name = str(name)
        self.description = str(description)
        self.type = str(type)
        self.quantity = int(quantity)
        # if quantity is None:
        #     self.quantity = 1
        # else:
        #     self.quantity = quantity
        self.price = price
        if id is None:
            self._id = uuid.uuid4().hex
        else:
            self._id = id

    def json_data(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "quantity": self.quantity,
            "price": self.price,
            "_id": self._id
        }

    # MONGO FUNCTION
    # def save_to_mongo(self):
    #     Database.insert(collection="item", data=self.json_data())

    def save_to_mongo(self):
        create_item_table()
        insert_item(name=self.name, description=self.description, type=self.type,
                    quantity=self.quantity, price=self.price, item_id=self._id)

    # mongo function to get all items
    # @staticmethod
    # def get_items():
    #     return [item for item in Database.find(collection="item")]

    @staticmethod
    def get_items():
        rows = view("item")
        row_list = []
        for row in rows:
            row_list.append({"item_id": row[1],
                             "name": row[2],
                             "description": row[3],
                             "type": row[4],
                             "quantity": row[5],
                             "price": row[6]})
        return row_list

    # mongo function to get item by id
    # @staticmethod
    # def get_item_by_id(id):
    #     return Database.find_one(collection="item", query={"_id": id})

    @staticmethod
    def get_item_by_id(id):
        rows = view_one("item", id)
        row = rows[0]
        return {"item_id": row[1],
                "name": row[2],
                "description": row[3],
                "type": row[4],
                "quantity": row[5],
                "price": row[6]}

    # mongo function to update item by id
    # @staticmethod
    # def update_item(id, data):
    #     Database.update_one(collection="item", query={"_id": id}, data=data)

    @staticmethod
    def update_item(id, data):
        quantity = description = name = type = price = None
        # print(quantity,description,name,type,price)

        if "name" in data:
            name = data["name"]
        if "description" in data:
            description = data["description"]
        if "type" in data:
            type = data["type"]
        if "quantity" in data:
            quantity = data["quantity"]
        if "price" in data:
            price = data["price"]

        data = view_one("item", id)
        data = data[0]
        if name is None:
            name = data[2]
        if description is None:
            description = data[3]
        if type is None:
            type = data[4]
        if quantity is None:
            quantity = data[5]
        if price is None:
            price = data[6]

        update_item(id=id, name=name, description=description, type=type, quantity=quantity, price=price)

    # mongo function for delete
    # @staticmethod
    # def delete_item(id):
    #     Database.delete_one(collection="item", query={"_id": id})

    @staticmethod
    def delete_item(id):
        delete_data("item", id)




