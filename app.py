from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Index(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dappa = db.Column(db.String(255))
    task = db.Column(db.Boolean)

@app.route('/')
def home():
    new = Index.query.all()
    return render_template("landing.html", new=new)

@app.route('/add', methods=['POST'])
def add():
    dappa = request.form.get("dappa")
    new_user = Index(dappa=dappa, task=False)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    new_task = Index.query.filter_by(id=todo_id).first()
    new_task.task = not new_task.task
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    new_task = Index.query.filter_by(id=todo_id).first()
    db.session.delete(new_task)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
