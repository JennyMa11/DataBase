from datetime import datetime

from sqlalchemy import Enum

from models import db


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    order_status = db.Column(Enum('已完成', '制作中','已下单',name = 'order_status'), default='已下单')

    # 关联关系
    user = db.relationship('User', backref='orders')