import uuid
from flask import Flask, jsonify, request,render_template
from flask_smorest import abort
from db import items,stores

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')


@app.post('/store')
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Ensure 'name' is in JSON Payload")

    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"store already exist")
    store_id = uuid.uuid4().hex

    store = {** store_data, "id": store_id}
    stores[store_id]= store
    return store, 201

@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message='store not found')


@app.get('/store')
def get_stores():
    return {'stores':list(stores.values())}

@app.post('/item')
def create_item():
    item_data = request.get_json()
    if (
        "name" not in item_data
        or "price" not in item_data
        or "store_id" not in item_data
    ):
        abort(400,
              message="Bad Request, Ensure 'name', 'price' and 'store_id' are in the Json Payload."
        )
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message='Item already exists')

    if item_data["store_id"] not in stores:
        abort(404, message='store not found')
    item_id = uuid.uuid4().hex

    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201

@app.get('/item')
def get_all_item():
    return {'items':list(items.values())}
@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message='store not found')

#app.run(debug=True)