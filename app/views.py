import os
import shutil
import uuid
from flask import (
    current_app,
    request,
    redirect,
    url_for,
    Blueprint,
    render_template,
    jsonify,
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from sqlalchemy.sql import exists
from datetime import datetime, timezone, timedelta
import threading
from .extensions import db
from .models import Upload


main_blueprint = Blueprint("main_blueprint", __name__)


@main_blueprint.route("/")
def home():
    return render_template("home.html")


@main_blueprint.route("/about")
def about():
    return render_template("about.html")


@main_blueprint.route("/upload", methods=["POST"])
def upload():
    while True:
        upload_id = str(uuid.uuid4()).replace("-", "")[:12]
        upload_directory = current_app.config["UPLOAD_DIRECTORY"] + upload_id + "/"
        upload_date = datetime.now(timezone.utc)

        if db.session.query(
            exists().where(Upload.directory == upload_directory)
        ).scalar():
            continue

        break

    try:
        file = request.files["file"]
        extention = os.path.splitext(file.filename)[1].lower()

        if file:
            if extention not in current_app.config["ALLOWED_EXTENSIONS"]:
                return jsonify({"message": "Not a vaild file type"})

            if not os.path.exists(upload_directory):
                os.makedirs(upload_directory)

            file.save(os.path.join(upload_directory, secure_filename(file.filename)))

    except RequestEntityTooLarge:
        return jsonify({"message": "File is larger than 16MB"}), 400

    try:
        new_upload = Upload(
            directory=upload_directory,
            created=upload_date,
            expiration=upload_date + (timedelta(minutes=10)),
        )
        db.session.add(new_upload)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return redirect(url_for("main_blueprint.display_file", query=upload_id))


@main_blueprint.route("/search")
def search():
    query = request.args.get("query", "")
    root = current_app.config["UPLOAD_DIRECTORY"]

    with os.scandir(root) as directories:
        for directory in directories:
            if directory.is_dir() and directory.name == query:
                return redirect(url_for("main_blueprint.display_file", query=query))

    return jsonify({"message": "Could not find " + directory.name})


@main_blueprint.route("/<query>", methods=["GET"])
def display_file(query):
    current_time = datetime.now(timezone.utc)
    expired_uploads = db.session.query(Upload).filter(Upload.expiration < current_time).all()

    for upload in expired_uploads:
        try:
            db.session.delete(upload)
            shutil.rmtree(upload.directory)
        except Exception as e:
            pass

    db.session.commit()

    directory = os.path.join(current_app.config["UPLOAD_DIRECTORY"], query)
    upload = db.session.query(Upload).filter_by(directory=directory)

    file = os.listdir(directory)
    if file:
        file = file[0]

    fileName = os.path.basename(file)
    fileSize = os.path.getsize(os.path.join(directory, file))

    directory = directory.removeprefix("app/")
    upload_id = query

    return render_template(
        "display-file.html",
        uploadId=upload_id,
        fileName=fileName,
        fileSize=fileSize,
        path=directory,
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
