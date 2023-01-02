import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
blp = Blueprint("stores", __name__, description="Operations on store")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message='store not found')

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(400, message="Bad Request, Store not found")




@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema )
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with name exists")
        except SQLAlchemyError:
            abort(500, message="Error while creating store")
        return store, 201
