from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///shoptest4.db"

db = SQLAlchemy(app=app)


class User(db.Model):
    __name__ = 'user'
    id = db.Column(db.VARCHAR, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False, )
    admin = db.Column(db.Integer)
    items = db.relationship("Item", cascade='all,delete', backref='user')

    def __init__(self, username, password, admin=0, id=None):
        self.username = username
        self.password = password
        self.admin = admin
        self.id = uuid.uuid4().hex if id is None else id

    def __repr__(self):
        return "<user %r>" % self.username


class Item(db.Model):
    __name__ = 'item'
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    type = db.Column(db.Text)
    price = db.Column(db.REAL)
    quantity = db.Column(db.FLOAT)
    id = db.Column(db.VARCHAR, primary_key=True)
    user_id = db.Column(db.VARCHAR, db.ForeignKey("user.id"))

    def __init__(self, name, description, type, price, user_id, quantity=1, id=None):
        self.name = name
        self.description = description
        self.type = type
        self.price = price
        self.quantity = quantity
        self.id = uuid.uuid4().hex if id is None else id
        self.user_id = user_id

db.create_all()
new_item = Item(name="Omo", description="detergent", type="small", price=50, user_id="75041953dd71404b9a2f13eba42f2c76")
# new_item2 = Item(name="Macbook", description="Laptop", type="2014", price=50000)
new_user = User(username="dimeji", password="dimeji")
new_user2 = User(username="tope", password="tope")

# db.session.add(new_user)
# db.session.add(new_user2)
# db.session.add(new_item)
# db.session.add(new_item2)

# user = User.query.filter_by(username="dimeji").first()
# print(user.items[0].name)
# db.session.delete(user)
# db.session.commit()

# item = Item.query.filter_by(name="Omo").first()
# print(item.name)

# db.session.delete(item)
# db.session.commit()
# print(user.items[0].name)


# print([i.name for i in Item.query.all()])


# def execute():
#     user = User.query.all()
#     for i in user:
#         print(i)
#
# execute()

# db.create_all()
# admin = Student(id=6, name='firststudent', age=20)
# db.session.add(admin)
# db.session.commit()

# print(Student.query.all())
# change_student = Student.query.filter_by(id=6).first()
# print(change_student)
# change_student.name = "superstudent"
# db.session.commit()

