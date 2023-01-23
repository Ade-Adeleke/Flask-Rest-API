from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.has import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", descriprion="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="Username has been taken")

        user = UserModel(
            username=user_data["username"]
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successful"}, 201