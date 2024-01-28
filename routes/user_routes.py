from flask import request, jsonify
from app import app
from models.User import *
from routes.functions import *
from models.Device import *


@app.route("/api/user/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if "name" not in data or "email" not in data or "password" not in data:
        return jsonify({"Message": "Invalid request"}), 400
    user = User.query.filter_by(email=data["email"]).first()
    if user:
        return jsonify({"Message": "User already exists"}), 400
    user = create_user_instance(data)
    response = add_user(user)
    print(response)
    return response


@app.route("/api/user/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user_agent = request.headers.get("User-Agent")
        if "email" not in data and "password" not in data:
            return jsonify({"Message": "Invalid request"}), 400
        user = check_user(data["email"], data["password"])
        if "device_name" not in data:
            if user:
                if user.is_active:
                    check_device = check_device_existence(user.id, user_agent)
                    if not check_device:
                        return jsonify({"Message": "Register This device"}), 203
                    else:
                        if check_device.isblocked:
                            return jsonify({"Message": "Device is blocked"}), 401
                        enable_device(check_device.id)
                        token = create_token(user, check_device.id)
                        return jsonify({"token": token}), 200
                else:
                    return jsonify({"Message": "User is blocked"}), 401
            else:
                return jsonify({"Message": "User does not exist"}), 404
        else:
            if user:
                if user.is_active:
                    device_data = {
                        "device_name": data["device_name"],
                        "user_agent": user_agent,
                        "user_id": user.id
                    }
                    device = create_device_instance(device_data)
                    device.user_id = user.id
                    device = add_device(device)
                    token = create_token(user, device.id )
                    return jsonify({"token": token}), 200
                else:
                    return jsonify({"Message": "User is blocked"}), 401
            else:
                return jsonify({"Message": "User does not exist"}), 404

    except Exception as e:
        return jsonify({"Message": str(e)}), 500


@app.route("/api/user", methods=["GET"])
def test():
    user_agent = request.headers.get("User-Agent")
    print("_____________USER AGENT_____________")
    print(user_agent)
    return jsonify({"Message": "Hello World"}), 200