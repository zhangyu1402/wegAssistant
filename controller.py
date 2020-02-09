from flask import Flask, request, jsonify
import json
import random
from tools import *
from flasgger import Swagger, swag_from
from mongo_connection import *

app = Flask(__name__)

Swagger(app)

db = get_db()

__ca = 1000
__caed = 0


@app.route('/api/<string:language>/', methods=['GET'])
def index(language):
    """
    This is the language awesomeness API
    Call this api passing a language name and get back its features
    ---
    tags:
      - Awesomeness Language API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """

    language = language.lower().strip()
    features = [
        "awesome", "great", "dynamic",
        "simple", "powerful", "amazing",
        "perfect", "beauty", "lovely"
    ]
    size = int(request.args.get('size', 1))
    if language in ['php', 'vb', 'visualbasic', 'actionscript']:
        return "An error occurred, invalid language for awesomeness", 500
    return jsonify(
        language=language,
        features=random.sample(features, size)
    )


@app.route('/products', methods=['GET'])
def get_all_products():
    """
       get all products
        ---
        tags:
          - Awesomeness Language API
        parameters:
          - name: page_size
            in: url
            type: string
            required: true
            description: page_size
          - name: page_num
            in: url
            type: string
            description: page_num
        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: a list of json
            schema:
              id: test
    """
    page_size = int(request.args.get("page_size"))
    page_num = int(request.args.get("page_num"))
    skio = page_size * (page_num - 1)

    res = list()
    for item in db['product'].find().limit(page_size).skip(skio):
        item.pop("_id")
        res.append(item)
    return json.dumps(res)


@app.route('/product/<id>', methods=['GET'])
def get_product_by_id(id):
    """
       get a product's infomation
        ---
        tags:
          - Awesomeness Language API
        parameters:
          - name: id
            in: path
            type: string
            required: true
            description: page_size
        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: json
            schema:
              id: awesome


    """
    product = db['product'].find_one({"sku": int(id)})
    product.pop("_id")
    return json.dumps(product)


@app.route('/calorie/<sku>', methods=['GET'])
def get_calorie_by_sku(sku):
    """
       get a product's calorie by sku
        ---
        tags:
          - Awesomeness Language API
        parameters:
          - name: sku
            in: path
            type: string
            required: true
            description: stock keep unit
        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: json
    """
    product = db['product'].find_one({"sku": int(sku)})
    ca = s_to_i(product['Calories'])
    return json.dumps(ca)


@app.route('/user/calorie/<user_id>/<sku>', methods=['POST'])
def buy_prodcut(user_id, sku):
    """
       update a user with sku
        ---
        tags:
          - Awesomeness Language API
        parameters:
          - name: sku
            in: path
            type: string
            required: true
            description: stock keep unit
        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: json
    """
    # product = db['users'].find_one({"sku":int(id)})
    # ca = s_to_i(product['Calories'])
    # return json.dumps()
    pass


@app.route('/user/<user_id>', methods=['GET'])
def check_user(user_id):
    """
       check if user exsit
        ---
        tags:
          - Awesomeness Language API
        parameters:
          - name: sku
            in: path
            type: string
            required: true
            description: stock keep unit
        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: number
    """
    user = db['users'].find_one({"user_id": user_id})

    return json.dumps(False if user is None else True)


@app.route('/calorie/', methods=['GET'])
def get_calorie():
    """
       get calorie of a list of sku
        ---
        tags:
          - Awesomeness Language API
        parameters:
          - name: skus
            in: url
            type: string
            required: true
            description: a list of sku
        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: number
    """
    skus = request.args.get("skus").split(",")
    res = []
    for sku in skus:
        product = db['product'].find_one({"sku": int(sku)})
        if product is None:
            print(sku)
        item = {"sku": sku, "name": product["name"]}

        if "Calories" in product:
            item["calories"] = product["Calories"]
        else:
            item["calories"] = -1
        res.append(item)
    return json.dumps(res)


@app.route('/user/standard/<user_id>', methods=['GET'])
def get_calorie_standard(user_id):
    """
       get calorie standard of a user
        ---
        tags:
          - Awesomeness Language API
        parameters:
          - name: user_id
            in: url
            type: string
            required: true
            description: user id
        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: number
    """
    standard = db['user'].find_one({"user_id": user_id})
    return json.dumps(standard)


@app.route('/user/history/<user_id>', methods=['GET'])
def get_calorie_history(user_id):
    """
       get calorie history of a user
        ---
        tags:
          - Awesomeness Language API
        parameters:
          - name: user_id
            in: url
            type: string
            required: true
            description: user id
        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: number
    """
    history = db['purchase'].find_one({"user_id": user_id})
    cal = 0
    for product in history['history']:
        product_info = db['product'].find_one({"sku": int(product['sku'])})
        cal += product_info["Calories"]
    return json.dumps(cal)


@app.errorhandler(Exception)
def all_exception_handler(e):

    return 'Error', 500


if __name__ == '__main__':
    app.debug = True
    app.run()
