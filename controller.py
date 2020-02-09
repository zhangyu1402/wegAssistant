from flask import Flask , request
import json

from mongo_connection import *
app = Flask(__name__)

@app.route('/products',methods=[ 'GET'])
def get_all_products():
    page_size = int(request.args.get("page_size"))
    page_num = int(request.args.get("page_num"))
    skio = page_size*(page_num-1)
    db = get_db()
    res = list()
    for item in db['product'].find().limit(page_size).skip(skio):
        item.pop("_id")
        res.append(item)
        # print(item)
    return json.dumps(res)

if __name__ == '__main__':
    app.debug = True
    app.run()