"""Flask Notes Application.

A small, full-stack notes management system with full CRUD support,
search, flash messaging and a custom 404 page.

Run locally with:
    pip install -r requirements.txt
    python app.py
"""

import os

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from models import Note, db


def create_app():
    """Application factory: build and configure the Flask app."""
    app = Flask(__name__)

    # Secret key is required for flash messages / sessions.
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-me")

    # Store the SQLite database inside the instance/ folder.
    os.makedirs(app.instance_path, exist_ok=True)
    db_path = os.path.join(app.instance_path, "notes.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Wire up the database and create tables on first run.
    db.init_app(app)
    with app.app_context():
        db.create_all()

    register_routes(app)
    register_error_handlers(app)

    return app


def register_routes(app):
    """Attach all view functions to the given app."""

    @app.route("/")
    def index():
        """Home page with a short summary of recent notes."""
        recent_notes = Note.query.order_by(
            Note.updated_at.desc()).limit(3).all()
        total_notes = Note.query.count()
        return render_template(
            "index.html",
            recent_notes=recent_notes,
            total_notes=total_notes,
        )

    @app.route("/notes")
    def notes():
        """List all notes, optionally filtered by a search query."""
        query = request.args.get("q", "", type=str).strip()

        notes_query = Note.query
        if query:
            like = f"%{query}%"
            notes_query = notes_query.filter(
                db.or_(Note.title.ilike(like), Note.content.ilike(like))
            )

        all_notes = notes_query.order_by(Note.updated_at.desc()).all()
        return render_template("notes.html", notes=all_notes, query=query)

    @app.route("/note/<int:note_id>")
    def view_note(note_id):
        """View a single note. 404 if the id does not exist."""
        note = Note.query.get_or_404(note_id)
        return render_template("view_note.html", note=note)

    @app.route("/add", methods=["GET", "POST"])
    def add_note():
        """Create a new note."""
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            content = request.form.get("content", "").strip()

            # Basic server-side validation.
            if not title or not content:
                flash("Both title and content are required.", "danger")
                return render_template(
                    "add_note.html", title=title, content=content
                )

            note = Note(title=title, content=content)
            db.session.add(note)
            db.session.commit()

            flash("Note created successfully.", "success")
            return redirect(url_for("view_note", note_id=note.id))

        return render_template("add_note.html", title="", content="")

    @app.route("/edit/<int:note_id>", methods=["GET", "POST"])
    def edit_note(note_id):
        """Edit an existing note. 404 if the id does not exist."""
        note = Note.query.get_or_404(note_id)

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            content = request.form.get("content", "").strip()

            if not title or not content:
                flash("Both title and content are required.", "danger")
                # Preserve the attempted edits in the form.
                note.title = title
                note.content = content
                return render_template("edit_note.html", note=note)

            note.title = title
            note.content = content
            # updated_at is refreshed automatically by the model's onupdate.
            db.session.commit()

            flash("Note updated successfully.", "success")
            return redirect(url_for("view_note", note_id=note.id))

        return render_template("edit_note.html", note=note)

    @app.route("/delete/<int:note_id>", methods=["POST"])
    def delete_note(note_id):
        """Delete a note. 404 if the id does not exist."""
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()

        flash("Note deleted successfully.", "success")
        return redirect(url_for("notes"))


def register_error_handlers(app):
    """Attach custom error handlers."""

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404


# Module-level app so `flask run` and `python app.py` both work.
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
