from app import app
from extensions import db

with app.app_context():
    db.drop_all()   # только для разработки!
    db.create_all()
    print("DB recreated")