"""Setup script to create a database if it does not exist."""
import os
from app import app, db_path
from data_models import db

if not os.path.exists(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with app.app_context():
        db.create_all()
