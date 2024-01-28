from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os 
from sqlalchemy.exc import SQLAlchemyError


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
app = Flask(__name__)
CORS(app)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    db = SQLAlchemy(app)
except SQLAlchemyError as e:
    app.logger.info("An error occurred during  db connection :", e)


ma = Marshmallow(app)
app.app_context().push()


from routes.user_routes import *
from routes.device_routes import *
from routes.admin_routes import *
from admin_creation import *

create_admin_user()

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")