from app import app
from flask import jsonify, request
from models.Device import *
from routes.functions import *
from models.User import *


@app.route("/api/admin/get_devices", methods=["GET"])
def retrieve_devices():
    try:
        payload = check_token(request.headers.get("Authorization"))
        user = User.query.filter_by(id=payload["id"]).first()
        print(user.is_admin)
        if user.is_admin:
            device = check_device_existence(user.id, request.headers.get("User-Agent"))
            users = get_all_users()
            users_to_return = []
            user_schema = UserSchema(many=True)
            for user in users:
                # user = user_schema.dump(user)
                # user.pop("password")
                devices = get_devices(user["id"])
                user["devices"] = devices
                users_to_return.append(user)
            return jsonify({"users": users , "device_id": device.id}), 200
        else:
            return jsonify({"Message": "Unauthorized"}), 401
    except Exception as e:
        return jsonify({"Message": str(e)}), 500


@app.route("/api/admin/validate", methods=["GET"])
def validate_admin():
    try:
        payload = check_token(request.headers.get("Authorization"))
        user = User.query.filter_by(id=payload["id"]).first()
        if user.is_admin:
            return jsonify({"isAdmin": "True"}), 200
        else:
            return jsonify({"isAdmin": "False"}), 200
    except Exception as e:
        return jsonify({"Message": str(e)}), 500


@app.route("/api/admin/block_device/<int:device_id>", methods=["DELETE"])
def block_device_by_admin(device_id):
    try:
        payload = check_token(request.headers.get("Authorization"))
        user = User.query.filter_by(id=payload["id"]).first()
        if user.is_admin:
            return block_device(device_id)
        else:
            return jsonify({"Message": "Unauthorized"}), 401
    except Exception as e:
        return jsonify({"Message": str(e)}), 500


@app.route("/api/admin/unblock_device/<int:device_id>", methods=["POST"])
def unblock_device_by_admin(device_id):
    try:
        payload = check_token(request.headers.get("Authorization"))
        user = User.query.filter_by(id=payload["id"]).first()
        if user.is_admin:
            return unblock_device(device_id)
        else:
            return jsonify({"Message": "Unauthorized"}), 401
    except Exception as e:
        return jsonify({"Message": str(e)}), 500


@app.route("/api/admin/logout_device/<int:device_id>", methods=["DELETE"])
def logout_device_by_admin(device_id):
    try:
        payload = check_token(request.headers.get("Authorization"))
        user = User.query.filter_by(id=payload["id"]).first()
        if user.is_admin:
            return disable_device_by_admin(device_id)
        else:
            return jsonify({"Message": "Unauthorized"}), 401
    except Exception as e:
        return jsonify({"Message": str(e)}), 500
    

@app.route("/api/admin/block_user/<int:user_id>", methods=["DELETE"])
def block_user_by_admin(user_id):
    try:
        payload = check_token(request.headers.get("Authorization"))
        user = User.query.filter_by(id=payload["id"]).first()
        user_to_block = User.query.filter_by(id=user_id).first()
        if user.is_admin:
            if user_to_block:
                user_to_block.is_active = False
                db.session.commit()
                return jsonify({"Message": "User blocked successfully"}), 200
            else:
                return jsonify({"Message": "User does not exist"}), 404
        else:
            return jsonify({"Message": "Unauthorized"}), 401
    except Exception as e:
        db.session.rollback()
        return jsonify({"Message": str(e)}), 500
    

@app.route("/api/admin/unblock_user/<int:user_id>", methods=["POST"])
def unblock_user_by_admin(user_id):
    try:
        payload = check_token(request.headers.get("Authorization"))
        user = User.query.filter_by(id=payload["id"]).first()
        user_to_unblock = User.query.filter_by(id=user_id).first()
        if user.is_admin:
            if user_to_unblock:
                user_to_unblock.is_active = True
                db.session.commit()
                return jsonify({"Message": "User blocked successfully"}), 200
            else:
                return jsonify({"Message": "User does not exist"}), 404
        else:
            return jsonify({"Message": "Unauthorized"}), 401
    except Exception as e:
        db.session.rollback()
        return jsonify({"Message": str(e)}), 500


@app.route("/api/admin/logout_user/<int:user_id>", methods=["DELETE"])
def logout_user_by_admin(user_id):
    try:
        payload = check_token(request.headers.get("Authorization"))
        user = User.query.filter_by(id=payload["id"]).first()
        user_to_logout = User.query.filter_by(id=user_id).first()
        if user.is_admin:
            if user_to_logout:
                devices = get_devices(user_to_logout.id)
                for device in devices:
                    disable_device_by_admin(device["id"])
                return jsonify({"Message": "User logged out successfully"}), 200
            else:
                return jsonify({"Message": "User does not exist"}), 404
        else:
            return jsonify({"Message": "Unauthorized"}), 401
    except Exception as e:
        db.session.rollback()
        return jsonify({"Message": str(e)}), 500