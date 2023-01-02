
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel, StoreModel
from sqlalchemy.exc import SQLAlchemyError
from db import db

blp = Blueprint("items", __name__, description="Operations on Items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message='store not found')

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message='item not found')

    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemSchema)
    def put(self, item_data ,item_id):

        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(400, message="item not found")


@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()



    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error occured while inserting the item")
        return item, 201