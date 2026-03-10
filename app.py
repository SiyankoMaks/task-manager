from flask import Flask, render_template
from config import Config
from extensions import db, login_manager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "auth.login"

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# подключение blueprints
from routes.auth import auth
from routes.tasks import tasks

app.register_blueprint(auth)
app.register_blueprint(tasks)

@app.route("/")
def home():
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)