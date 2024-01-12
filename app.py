from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'key'

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False, unique=True)

class Form(FlaskForm):
    nome = StringField('Nome')
    salvar = SubmitField('Salvar')
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/form', methods=['GET', 'POST'])
def store():
    form = Form()
    if request.method == 'POST' and form.validate_on_submit():
        nome = form.nome.data
        new_task = Task(nome=nome)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html', form=form)

@app.route('/create', methods=['GET', 'POST'])
def create():
    return redirect(url_for('store'))

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
