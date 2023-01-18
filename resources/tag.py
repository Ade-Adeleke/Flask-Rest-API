from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas import TagSchema, TagAndItemSchema
from models import TagModel,ItemTagsModel, StoreModel, ItemModel
from sqlalchemy.exc import SQLAlchemyError
from db import db

blp = Blueprint("tags", __name__, description="Operations on Tags")

@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tag.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self,tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    def delete(self, tag_id):
        tag = ItemModel.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return {"message": "Tag deleted"}

blp.route("/item/<string:store_id>/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, tag_id, item_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tag.append(tag)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag

    @blp.response(200, TagSchema)
    def delete(self, tag_id, item_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tag.remove(tag)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return {"message": "item unlinked from tag"}

