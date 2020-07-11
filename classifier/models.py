from datetime import datetime
from classifier import db
from flask_login import UserMixin


class User(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    image_file =db.Column(db.String(20), nullable=False, default='default.jpg')
    label = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pred_class = db.Column(db.String, default = '')

    def __repr__(self):
        return f"User('{self.image_file}', '{self.label}', '{self.date}')"
