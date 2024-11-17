from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Tasks:
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String(100), nullable=False)
    finished = db.Column(db.Boolean)
    categoty = db.Column(db.String(50), default="Other")
    deadline = db.Column(db.DateTime)