from flask import flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_required
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, AdminIndexView, expose

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        if not current_user.is_authenticated:
            flash('You are not authorized to access this page', 'error')
            return redirect('/')
        return super(MyAdminIndexView, self).index()

db = SQLAlchemy()
admin = Admin(index_view=MyAdminIndexView())

# user_roles = db.Table(
#     'user_roles',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
#     db.Column('name', db.Text)
# )

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    users = db.relationship('User', back_populates="role")
    
    def __repr__(self):
        return self.name
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    role = db.relationship('Role', back_populates="users")
    role_id = db.Column(db.ForeignKey('role.id'), default=2)
    

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated;
    
class UserView(AdminView):
    form_columns = ['name', 'email', 'password', 'role']
    column_list= ['name', 'email', 'role']
    
class RoleView(AdminView):
    form_columns = ['name', 'description']
    column_list= ['name', 'description']
    
admin.add_view(UserView(User, db.session))
admin.add_view(RoleView(Role, db.session))