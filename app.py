from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/form')
def store():
    return render_template('form.html')

@app.route('/create', methods=['POST'])
def create():
    task_nome = request.form.get('nome')  
    new_task = Task(nome=task_nome) 
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>')
def edit(task_id):
    task = Task.query.get(task_id)
    return render_template('edit.html', task=task, task_id=task_id)

@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    task = Task.query.get(task_id)
    task.nome = request.form.get('nome')  # Ajuste para 'nome' em vez de 'task'
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
