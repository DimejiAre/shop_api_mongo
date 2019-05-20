from common.database import Database
from models.user import User
from models.Item import Item
from functools import wraps
from flask import Flask, request, make_response, jsonify
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

Database.initialize()

app.config['SECRET_KEY'] = 'secretkey'


def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "token" in request.headers and request.headers["token"]:
            token = request.headers["token"]
            try:
                jwt_data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = User.get_userclass_by_id(user_id=jwt_data["_id"])
                return f(current_user, *args, **kwargs)
            except:
                return jsonify({"message": "Token Invalid"})
        else:
            return jsonify({"message": "No token found [token: <token string>]"})
            # return make_response("Could not verify!", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated


@app.route("/store/api/v1")
def index():
    return "Welcome to my shop API"


@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    try:
        name = request.json["username"]
        user = User.get_userclass_by_username(name=name)
        user_json = user.json_data()
        user_json["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=50)
        if check_password_hash(user.password, request.json["password"]) and user.admin is 1:
            token = jwt.encode(payload=user_json, key=app.config['SECRET_KEY'])
            return jsonify({"token": token.decode('UTF-8')})
        elif check_password_hash(user.password, request.json["password"]) and user.admin is 0:
            token = jwt.encode(payload=user_json, key=app.config['SECRET_KEY'])
            return jsonify({"token": token.decode('UTF-8')})
        else:
            return make_response("Login Failed!", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    except:
        return make_response("Could not verify!", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route("/api/v1/item", methods=['GET'])
def view_items():
    items = Item.get_items()
    if not items:
        return jsonify({"message": "No items found"})
    return jsonify({"items": items})


@app.route("/api/v1/item/<item_id>", methods=['GET'])
def view_one_item(item_id):
    item = Item.get_item_by_id(id=item_id)
    if not item:
        return jsonify({"message": "Item does not exist"})
    return jsonify(item)
    # return json.dumps(item)


@app.route("/api/v1/item", methods=['POST'])
@require_token
def create_item(current_user):
    if current_user.admin is False:
        return jsonify({"message": "You are not authorised to perform this function"})
    try:
        r = request.json
        item = Item(name=r['name'], description=r['description'], type=r['type'], price=r['price'], quantity=r['quantity'])
        item.save_to_mongo()
        return jsonify({"message": "{} Created".format(item.name)})
    except:
        return jsonify({"message": "An error occurred, Item could not be created"})


@app.route("/api/v1/item/<item_id>", methods=['PUT'])
@require_token
def update_item(current_user, item_id):
    if current_user.admin is False:
        return jsonify({"message": "You are not authorised to perform this function"})
    item = Item.get_item_by_id(id=item_id)
    if not item:
        return jsonify({"message": "Item does not exist"})
    try:
        r = request.json
        Item.update_item(id=item_id, data=r)
        return jsonify({"message": "Item updated"})
    except:
        return jsonify({"message": "An error occurred, Item could not be updated"})


@app.route("/api/v1/item/buy/<item_id>", methods=['PUT'])
def buy(item_id):
    try:
        item = Item.get_item_by_id(id=item_id)
        if not item:
            return jsonify({"message": "Item does not exist"})

        if request.data and request.json["quantity"]:
            quantity = int(request.json["quantity"])
        else:
            quantity = 1
        item["quantity"] -= quantity
        Item.update_item(id=item_id, data=item)
        return jsonify({"message": "{} unit(s) of {} Purchased".format(quantity, item["name"])})
    except:
        return jsonify({"message": "An error occurred, Item could not be purchased"})


@app.route("/api/v1/item/<item_id>", methods=['DELETE'])
@require_token
def delete_item(current_user, item_id):
    if current_user.admin is False:
        return jsonify({"message": "You are not authorised to perform this function"})
    # r = request.json
    item = Item.get_item_by_id(id=item_id)
    if not item:
        return jsonify({"message": "Item does not exist"})
    try:
        Item.delete_item(id=item_id)
        return jsonify({"message": "{} deleted".format(item["name"])})
    except:
        return jsonify({"message": "An error occurred, Item could not be deleted"})


@app.route("/api/v1/user", methods=['GET'])
@require_token
def view_users(current_user):
    if current_user.admin is False:
        return jsonify({"message": "You are not authorised to perform this function"})
    users = User.get_users()
    if not users:
        return jsonify({"message": "No user to display"})
    return jsonify({"users": users})


@app.route("/api/v1/user/<user_id>", methods=['GET'])
@require_token
def view_one_user(current_user, user_id):
    if current_user.admin is False:
        return jsonify({"message": "You are not authorised to perform this function"})
    user = User.get_user_by_id(id=user_id)
    if not user:
        return jsonify({"message": "No user to display"})
    return jsonify({"message": user})


@app.route("/api/v1/user", methods=['POST'])
def create_user():
    try:
        r = request.json
        user = User(username=r["username"], password=generate_password_hash(r["password"],'sha1'), admin=False)
        user.save_to_mongo()
        return jsonify({"message": "User({}) created".format(user.username)})
    except:
        return jsonify({"message": "An error occurred when creating user"})


@app.route("/api/v1/user/promote/<user_id>", methods=['PUT'])
@require_token
def promote_user(user_id):
    # if current_user.admin is False:
    #     return jsonify({"message": "You are not authorised to perform this function"})
    try:
        user = User.get_userclass_by_id(user_id=user_id)
        User.update_user_by_id(id=user_id, data={"admin": True})
        return jsonify({"message": "{} is now an admin".format(user.username)})
    except:
        return jsonify({"message": "An error occurred when promoting user"})


@app.route("/api/v1/user/<user_id>", methods=['DELETE'])
@require_token
def delete_user(current_user, user_id):
    if current_user.admin is False:
        return jsonify({"message": "You are not authorised to perform this function"})
    user = User.get_user_by_id(id=user_id)
    if not user:
        return jsonify({"message": "User does not exist"})
    try:
        User.delete_user_by_id(id=user_id)
        return jsonify({"message": "{} has been deleted".format(user["username"])})
    except:
        return jsonify({"message": "An error occurred when deleting user"})


if __name__ == '__main__':
    app.run(debug=True)




