from .extensions import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    directory = db.Column(db.String(120), unique=True, nullable=False)
    created = db.Column(
        db.DateTime, default=datetime.now(timezone.utc), unique=False, nullable=False
    )
    expiration = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc) + (timedelta(minutes=10)),
        unique=False,
        nullable=False,
    )
