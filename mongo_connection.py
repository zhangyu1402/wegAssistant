import pymongo



def get_db():
    client = pymongo.MongoClient(
        "mongodb+srv://yzh269:xw18813086938@xzz-prjx3.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    print(client)
    db = client['hackathon']
    return db


def store(collection, data):
    collection.insert_one(data)


if __name__ == '__main__' :
    db = get_db()
    db['categories'].insert_one({"test":"test"})
    # print(db.list_collection_names())
    # store(db['products'],{'a':'b'})