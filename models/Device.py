from app import db, ma
from flask import jsonify

class Device(db.Model):
    __tablename__ = "device"
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(), nullable=False)
    user_agent = db.Column(db.String(), nullable=False)
    isactive = db.Column(db.Boolean, default=True)
    isblocked = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Device {self.device_name}>"
    

class DeviceSchema(ma.Schema):
    class Meta:
        fields = ("id", "device_name", "isactive", "user_id", "isblocked", "user_agent")


def create_device_instance(data):
    device = Device()
    device.device_name = data["device_name"]
    device.user_agent = data["user_agent"]
    device.user_id = data["user_id"]
    return device


def add_device(device):
    try:
        db.session.add(device)
        db.session.commit()
        return device
    except Exception as e:
        raise e

def get_devices(user_id):
    try:
        devices = Device.query.filter_by(user_id=user_id).all()
        device_schema = DeviceSchema(many=True)
        return device_schema.dump(devices)
    except Exception as e:
        raise e


def get_device(device_id):
    try:
        device = Device.query.filter_by(id=device_id).first()
        device_schema = DeviceSchema()
        return jsonify(device_schema.dump(device)), 200
    except Exception as e:
        return jsonify({"Message": str(e)}), 500
    

def delete_device(device_id, user_id):
    try:
        device = Device.query.filter_by(id=device_id).first()
        if not device:
            raise Exception("Device does not exist")
        if device.user_id != user_id:
            raise Exception("Unauthorized")
        db.session.delete(device)
        db.session.commit()
        return jsonify({"Message": "Device deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        raise e


def update_device(device_id, data):
    try:
        device = Device.query.filter_by(id=device_id).first()
        device.device_name = data["device_name"]
        device.user_agent = data["user_agent"]
        db.session.commit()
        return jsonify({"Message": "Device updated successfully"}), 200
    except Exception as e:
        return jsonify({"Message": str(e)}), 500
    

def disable_device(device_id, user_id):
    try:
        device = Device.query.filter_by(id=device_id).first()
        if not device:
            raise Exception("Device does not exist")
        if device.user_id == user_id:
            device.isactive = False
            db.session.commit()
            return jsonify({"Message": "Device disabled successfully"}), 200
        else:
            raise Exception("You are not authorized to perform this action")
    except Exception as e:
        db.session.rollback()
        return jsonify({"Message": str(e)}), 500


def enable_device(device_id):
    try:
        device = Device.query.filter_by(id=device_id).first()
        device.isactive = True
        db.session.commit()
        return True
    except Exception as e:
        raise e

def check_device_existence(user_id, user_agent):
    try:
        device = Device.query.filter_by(user_id=user_id, user_agent=user_agent).first()
        if device:
            return device
        return None
    except Exception as e:
        raise e
    
def get_all_devices():
    try:
        devices = Device.query.all()
        device_schema = DeviceSchema(many=True)
        return device_schema.dump(devices)
    except Exception as e:
        raise e


def block_device(device_id):
    try:
        device = Device.query.filter_by(id=device_id).first()
        if device:
            device.isblocked = True
            device.isactive = False
            db.session.commit()
            return jsonify({"Message": "Device blocked successfully"}), 200
        else:
            return jsonify({"Message": "Device does not exist"}), 404
    except Exception as e:
        db.session.rollback()
        raise e


def unblock_device(device_id):
    try:
        device = Device.query.filter_by(id=device_id).first()
        if device:
            device.isblocked = False
            db.session.commit()
            return jsonify({"Message": "Device unblocked successfully"}), 200
        else:
            return jsonify({"Message": "Device does not exist"}), 404
    except Exception as e:
        db.session.rollback()
        raise e
    

def disable_device_by_admin(device_id):
    try:
        device = Device.query.filter_by(id=device_id).first()
        if device:
            device.isactive = False
            db.session.commit()
            return jsonify({"Message": "Device disabled successfully"}), 200
        else:
            return jsonify({"Message": "Device does not exist"}), 404
    except Exception as e:
        db.session.rollback()
        raise e
