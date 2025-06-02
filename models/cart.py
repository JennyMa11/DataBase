from models import db


class Cart(db.Model):
    __tablename__ = 'carts'

    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.food_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)

    # 关联关系
    user = db.relationship('User', backref='cart_items')
    food = db.relationship('Food', backref='cart_items')