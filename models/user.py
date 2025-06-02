from flask_login import UserMixin
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from models import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15))
    role = db.Column(Enum('admin', 'user', name='user_roles'), default='user')

    # Flask-Login 需要的方法
    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
