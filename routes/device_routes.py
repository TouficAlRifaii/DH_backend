from app import app
from flask import jsonify, request
from models.Device import *
from routes.functions import *
from models.User import *


@app.route("/api/device/get_all", methods=["GET"])
def get_all_devices():
    try:
        payload = check_token(request.headers.get("Authorization"))
        user = User.query.filter_by(id=payload["id"]).first()

        if user:
            check_device = check_device_existence(
                user.id, request.headers.get("User-Agent")
            )
            if not check_device.isactive:
                return jsonify({"Message": "Unauthorized"}), 401
            devices = get_devices(user.id)
            print(devices)
            return jsonify({"devices": devices, "device_id": check_device.id}), 200
        else:
            return jsonify({"Message": "User does not exist"}), 400
    except Exception as e:
        return jsonify({"Message": str(e)}), 500


@app.route("/api/device/get/<int:device_id>", methods=["GET"])
def get_device(device_id):
    try:
        payload = check_token(request.headers.get("Authorization"))
        user = User.query.filter_by(id=payload["id"]).first()
        if user:
            device = get_device(device_id)
            return jsonify({"device": device}), 200
        else:
            return jsonify({"Message": "User does not exist"}), 400
    except Exception as e:
        return jsonify({"Message": str(e)}), 500


@app.route("/api/device/logout/<int:device_id>", methods=["DELETE"])
def logout_device(device_id):
    try:
        payload = check_token(request.headers.get("Authorization"))
        user = User.query.filter_by(id=payload["id"]).first()
        if user:
            return disable_device(device_id, user.id)
        else:
            return jsonify({"Message": "User does not exist"}), 400
    except Exception as e:
        return jsonify({"Message": str(e)}), 500


@app.route("/api/device/delete/<int:device_id>", methods=["DELETE"])
def delete_device_route(
    device_id,
):
    try:
        payload = check_token(request.headers.get("Authorization"))
        user = User.query.filter_by(id=payload["id"]).first()
        if user:
            return delete_device(device_id, user.id)
        else:
            return jsonify({"Message": "User does not exist"}), 400
    except Exception as e:
        return jsonify({"Message": str(e)}), 500
