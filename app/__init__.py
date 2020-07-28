from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import config_manager as cfg


server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = cfg.get_postgresql_url()
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)

from app import views
from app.databases import models
