from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

from models import User, Task

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

@app.route("/")
def home():
    return "Task Manager is running with PostgreSQL!"

if __name__ == "__main__":
    app.run(debug=True)