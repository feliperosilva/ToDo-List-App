from flask import Flask, render_template, redirect, url_for, request
from models import db, Tasks
from datetime import datetime, date, timedelta

#Conection to database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/mytasks.db'
db.init_app(app)

with app.app_context():
    db.create_all()

#main route 
#display tasks
#filters by category, status and deadline range
@app.route('/')
def home():
    all_tasks = Tasks.query.all()

    category = request.args.get('category')
    finished = request.args.get('finished')
    deadline = request.args.get('deadline')

    today = date.today()

    query = Tasks.query

    if category == '':
        category = None

    if deadline == '':
        deadline = None

    if category and category != '':
        query = query.filter(Tasks.category == category)

    if finished == '':
        pass

    if finished == 'Finished':
        query = query.filter(Tasks.finished == True)

    if finished == 'Unfinished':
        query = query.filter(Tasks.finished == False)
    
    if deadline == 'a week':
        week_deadline = today + timedelta(days=7)
        query = query.filter(Tasks.deadline <= week_deadline)
    
    elif deadline == '15 days':
        fifteen_days_deadline = today + timedelta(days=15)
        query = query.filter(Tasks.deadline <= fifteen_days_deadline)
    
    elif deadline == 'a month':
        month_deadline = today + timedelta(days=30)
        query = query.filter(Tasks.deadline <= month_deadline)

    all_tasks = query.all()

    return render_template('index.html', all_tasks=all_tasks)

#route with a POST method to create a new task
@app.route('/create_task', methods=['POST'])
def create_task():
    content = request.form.get('content')
    category = request.form.get('category')
    deadline = request.form.get('deadline')

    if category == '':
        category = None
    
    if deadline == '':
        deadline = None
    else:
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()

    task = Tasks (
        content=content,
        category=category,
        deadline=deadline
    )

    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))

#route to mark a task as finished
@app.route('/finished_task/<id>')
def finished_task(id):
    task = Tasks.query.get(int(id))
    if task:
        task.finished = not task.finished
    db.session.commit()
    return redirect(url_for('home'))

#route to delete a task
@app.route('/delete_task/<id>')
def delete_task(id):
    task = Tasks.query.get(int(id))
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
