from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Tasks(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String(100), nullable=False)
    finished = db.Column(db.Boolean, default = False)
    category = db.Column(db.String(50))
    deadline = db.Column(db.Date)