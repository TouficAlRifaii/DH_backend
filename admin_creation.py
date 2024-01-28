from models.User import User, add_user, check_user, create_user_instance
from dotenv import load_dotenv
import os


load_dotenv()
admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")


def create_admin_user():
    admin_user = User.query.filter_by(email=admin_email).first()
    if admin_user is None:
        admin_user = create_user_instance(
            {
                "name": "Admin",
                "email": admin_email,
                "password": admin_password,
                "is_admin": True,
            }
        )
        add_user(admin_user)
        print("Admin user created successfully")
    else:
        pass
