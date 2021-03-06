import requests
import const
import json
import logging
import time
from mongo_connection import *
from tools import *
from threading import Timer
payload = {
           'Subscription-Key': const.Subscription_Key}
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
def grab_product(url):
    try:
        response = requests.get(url, params=payload)
        result = json.loads(response.text)
        if 'nutrients' in result:
            for nus in result['nutrients']:
                nus_type = nus['type']
                quantity  = s_to_i(nus['quantity'])
                result[nus_type] = quantity
            result.pop("nutrients")
        result.pop("_links")
        result.pop("states")
        db = get_db()
        store(db['product'],result)
    except Exception:
        print("error")


def grab_sub_cat(url,colloction):
    response = requests.get(url, params=payload)
    result = json.loads(response.text)
    if 'categories' in result:
        tmplist = result['categories']
        tmplist.reverse()
        for cat in tmplist:

            time.sleep(0.5)

            logging.info('start to grab cat : {}'.format(cat["name"]))
            # print('start to grab cat : ',cat["name"])
            grab_sub_cat("https://api.wegmans.io"+cat["_links"][0]["href"],colloction[cat["name"]])
    if "products" in result:
        for pro in result["products"]:
            store(colloction, pro)
            logging.info('start to grab products {}'.format(pro["name"]))
            grab_product("https://api.wegmans.io"+pro["_links"][0]["href"])


def grab_all_categories():
    url = "https://api.wegmans.io/products/categories?api-version=2018-10-18"

    # response = requests.get(url, params=payload)
    # categories = json.loads(response.text)
    # for cat in categories['categories']:
    #     logging.info('start to grab {}',cat["name"])
    #     grab_sub_cat("https://api.wegmans.io"+cat["_links"][0]["href"])
    db = get_db()
    grab_sub_cat(url,db.categories)

if __name__ == '__main__' :
    pass

    grab_all_categories()
    grab_tast = Timer(60*60*24,grab_all_categories)
    grab_tast.start()
    grab_tast.join()

# logging.info('start to grab cat{}')