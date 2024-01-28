import jwt
from app import SECRET_KEY

def create_token(user, device_id):
    payload = {
        "id": user.id,
        "is_admin": user.is_admin,
        "device_id": device_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def check_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise Exception("Expired Token")
    except jwt.InvalidTokenError as e :
        raise Exception("Invalid Token")
    except Exception as e:
        raise e
