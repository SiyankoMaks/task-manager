from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from extensions import db
from models import Task

tasks = Blueprint("tasks", __name__)

@tasks.route("/tasks")
@login_required
def tasks_page():

    user_tasks = Task.query.filter_by(user_id=current_user.id).all()

    return render_template("tasks.html", tasks=user_tasks)


@tasks.route("/add_task", methods=["POST"])
@login_required
def add_task():

    title = request.form["title"]

    task = Task(title=title, user_id=current_user.id)

    db.session.add(task)
    db.session.commit()

    return redirect(url_for("tasks.tasks_page"))