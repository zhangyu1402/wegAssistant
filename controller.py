from flask import Flask , request
import json
from tools import *

from mongo_connection import *
app = Flask(__name__)


db = get_db()

__ca = 1000
__caed = 800
@app.route('/products',methods=[ 'GET'])
def get_all_products():
    page_size = int(request.args.get("page_size"))
    page_num = int(request.args.get("page_num"))
    skio = page_size*(page_num-1)

    res = list()
    for item in db['product'].find().limit(page_size).skip(skio):
        item.pop("_id")
        res.append(item)
    return json.dumps(res)


@app.route('/calorie/<id>',methods=[ 'GET'])
def get_nutrition(id) :
    product = db['product'].find_one({"sku":int(id)})
    ca = s_to_i(product['Calories'])
    return json.dumps((__caed+ca)/__ca)


if __name__ == '__main__':
    app.debug = True
    app.run()