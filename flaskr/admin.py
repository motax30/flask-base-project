from flask_admin import Admin
from flask_admin.contrib import sqla
from flaskr.views.admin_index_view import MyAdminIndexView
from flaskr.models.user import UserModel
from flaskr.db import db_instance as db
import flask_login as login

class UserModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        # return redirect(url_for('login', next=request.url))
        return False

def config_flask_admin(app):
    # set optional bootswatch theme
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='Admin Example', index_view=MyAdminIndexView(), base_template='my_master.html', template_mode='bootstrap3')

    admin.add_view(UserModelView(UserModel, db.session))

    return admin