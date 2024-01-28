from app import db, ma, app
from flask_bcrypt import Bcrypt
from flask import jsonify

bcrypt = Bcrypt(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    def __str__(self):
        return self.name


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ("id", "name", "email", "is_admin", "is_active", "timestamp")


def create_user_instance(jsonObject):
    user = User(
        name=jsonObject["name"],
        email=jsonObject["email"],
        password=bcrypt.generate_password_hash(jsonObject["password"]).decode("utf-8"),
    )
    if "is_admin" in jsonObject:
            user.is_admin = jsonObject["is_admin"]
    if "is_active" in jsonObject:
        user.is_active = jsonObject["is_active"]
    return user


def add_user(user):
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"Message": "User added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"Message": "Internal Server Error"}), 500


def check_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user is None:
        raise Exception("User does not exist")
    if not user.is_active:
        raise Exception("This user is banned")
    if not bcrypt.check_password_hash(user.password, password):
        raise Exception("Invalid credentials")
    return user


def get_all_users():
    try:
        users = User.query.all()
        user_schema = UserSchema(many=True)
        return user_schema.dump(users)
    except Exception as e:
        raise e
