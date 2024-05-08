from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from website.auth import users

tasks = []
task_manager = Blueprint("task_manager", __name__)

@task_manager.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        # Access the logged-in user via current_user
        return render_template('index.html', tasks=tasks, username=current_user.username)
    else:
        return redirect(url_for('auth.login'))

@task_manager.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if current_user.is_authenticated:
        task = request.form['task']
        priority = request.form['priority']
        tasks.append({'name': task, 'done': False, 'priority': priority})
        return redirect(url_for('task_manager.index'))

    else:
        return redirect(url_for('auth.login'))

@task_manager.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if current_user.is_authenticated:
        if request.method == 'POST':
            updated_task = request.form['task']
            updated_priority = request.form['priority']
            tasks[index]['name'] = updated_task
            tasks[index]['priority'] = updated_priority
            return redirect(url_for('task_manager.index'))
        else:
            return render_template('edit.html', task_name=tasks[index]['name'])
    else:
        return redirect(url_for('auth.login'))

@task_manager.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    if current_user.is_authenticated:
        del tasks[index]
        return redirect(url_for('task_manager.index'))
    else:
        return redirect(url_for('auth.login'))

@task_manager.route('/mark_done/<int:index>', methods=['POST'])
def mark_done(index):
    if current_user.is_authenticated:
        tasks[index]['done'] = True
        return redirect(url_for('task_manager.index'))
    else:
        return redirect(url_for('auth.login'))