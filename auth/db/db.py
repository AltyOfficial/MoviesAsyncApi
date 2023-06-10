from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from auth.utils.settings import settings


db = SQLAlchemy()

pg_user = settings.USERNAME
pg_pass = settings.PASSWORD
pg_host = settings.HOST
pg_port = settings.PORT
pg_db = settings.DATABASE_NAME

SQLALCHEMY_DATABASE_URI=f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app) 
