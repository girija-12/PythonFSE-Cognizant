class Config:
    SECRET_KEY = "coursemanager-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///coursemanager.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False