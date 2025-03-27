import os


class Config:
    UPLOAD_DIRECTORY = "app/static/files/uploads/"
    SECRET_KEY = os.urandom(12)
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {
        ".png",
        ".jpeg",
        ".jpg",
        ".gif",
        ".svg",
        ".webp",
        ".css",
        ".js",
        ".html",
        ".htm",
        ".woff",
        ".woff2",
        ".ttf",
        ".otf",
        ".mp3",
        ".ogg",
        ".wav",
        ".aac",
        ".mp4",
        ".webm",
        ".ogg",
        ".pdf",
        ".txt",
        ".docx",
        ".xlsx",
        ".zip",
        ".tar.gz",
        ".tar.bz2",
        ".tar.xz",
        ".php",
        ".py" ".rust",
        ".c",
        ".h",
        ".cpp",
        ".hpp",
    }
