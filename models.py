"""Database models for the Notes application."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

# Single SQLAlchemy instance, initialised in app.py via db.init_app(app).
db = SQLAlchemy()


class Note(db.Model):
    """A single note owned by the application."""

    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # created_at is set once on insert; updated_at is refreshed on every change.
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self):
        return f"<Note {self.id}: {self.title!r}>"
