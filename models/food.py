from models import db


class Food(db.Model):
    __tablename__ = 'foods'

    food_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(5, 2), nullable=False)
    image_url = db.Column(db.String(255))