from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from extensions import db
from models import Task
from datetime import datetime

tasks = Blueprint("tasks", __name__)

def apply_filters(query):
    status = request.args.get("status")
    priority = request.args.get("priority")
    search = request.args.get("search")

    if status in ["pending", "done"]:
        query = query.filter_by(status=status)

    if priority in ["low", "medium", "high"]:
        query = query.filter_by(priority=priority)

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    return query

@tasks.route("/tasks")
@login_required
def tasks_page():

    query = Task.query.filter_by(user_id=current_user.id)

    # --- FILTERS ---
    query = apply_filters(query)

    # --- SORT ---
    sort = request.args.get("sort")
    order = request.args.get("order", "asc")

    if sort == "deadline":
        query = query.order_by(
            Task.deadline.desc() if order == "desc" else Task.deadline.asc()
        )
    elif sort == "created":
        query = query.order_by(
            Task.created_at.desc() if order == "desc" else Task.created_at.asc()
        )
    
    if order not in ["asc", "desc"]:
        order = "asc"

    # --- PAGINATION ---
    page = request.args.get("page", 1, type=int)

    tasks = query.paginate(page=page, per_page=5)

    args = request.args.to_dict()
    args.pop("page", None)

    return render_template("tasks.html", tasks=tasks, args=args)

@tasks.route("/add_task", methods=["POST"])
@login_required
def add_task():
    title = request.form["title"]
    description = request.form.get("description")
    priority = request.form.get("priority", "medium")

    deadline_str = request.form.get("deadline")

    deadline = None
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            deadline = None

    task = Task(
        title=title,
        description=description,
        priority=priority,
        deadline=deadline,
        user_id=current_user.id
    )

    db.session.add(task)
    db.session.commit()

    return redirect(url_for("tasks.tasks_page"))


@tasks.route("/tasks/delete/<int:id>", methods=["POST"])
@login_required
def delete_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for("tasks.tasks_page"))


@tasks.route("/tasks/done/<int:id>")
@login_required
def mark_done(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    task.status = "done"
    db.session.commit()

    return redirect(url_for("tasks.tasks_page"))


@tasks.route("/tasks/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        task.title = request.form["title"]
        task.description = request.form.get("description")
        task.priority = request.form.get("priority")
        task.deadline = request.form.get("deadline")

        db.session.commit()
        return redirect(url_for("tasks.tasks_page"))

    return render_template("edit_task.html", task=task)