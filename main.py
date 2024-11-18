from flask import Flask, render_template, redirect, url_for, request
from models import db, Tasks
from datetime import date, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/mytasks.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    all_tasks = Tasks.query.all()

    if request.method == 'POST':
        category = request.form.get('category')
        finished = request.form.get('finished')
        deadline = request.form.get('deadline')

        today = date.today()

        query = Tasks.query

        if category and category != '':
            query = query.filter(category=category)

        if finished and finished != '':
            query = query.filter(finished=finished)
        
        if deadline == 'a week':
            week_deadline = today + timedelta(days=7)
            query = query.filter(Tasks.deadline <= week_deadline)
        
        elif deadline == '15 days':
            fifteen_days_deadline = today + timedelta(days=15)
            query = query.filter(Tasks.deadline <= fifteen_days_deadline)
        
        elif deadline == 'a month':
            month_deadline = today + timedelta(days=30)
            query = query.filter(Tasks.deadline <= month_deadline)

    return render_template('index.html', all_tasks=all_tasks, category=category, finished=finished, deadline=deadline)

@app.route("/create_task", methods=['POST'])
def create_task():
    task = Tasks (
        content = request.form['content'],
        category = request.form['category'],
        deadline = date.strptime(request.form['deadline'], '%Y-%m-%d').date()
        if request.form['deadline'] else None
    )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/finished_task")
def finished_task(id):
    task = Tasks.query.get(int(id))
    if task:
        task.finished = not task.finished
    db.session.commit()
    return redirect(url_for('home'))

