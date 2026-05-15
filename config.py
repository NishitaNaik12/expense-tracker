import os

class Config:
    # Handle the fact that Render/Heroku often provide 'postgres://' 
    # but SQLAlchemy 1.4+ requires 'postgresql://'
    database_url = os.environ.get('DATABASE_URL') or 'sqlite:///expenses.db'
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
