from flask_login import LoginManager
from flaskr.db import db_instance as db
from flaskr.models import UserModel
def config_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(UserModel).get(user_id)

    return login_manager