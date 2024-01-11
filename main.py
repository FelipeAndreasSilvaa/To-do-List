from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def home():
    # show all todos
    todo_list = Todo.query.all()
    return render_template('home/home.html', todo_list=todo_list)

@app.route('/add', methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # add new item
    new_todo = Todo.query.filter_by(id=todo_id).first()
    new_todo.complete = not new_todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # add new item
    new_todo = Todo.query.filter_by(id=todo_id).first
    db.session.delete(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    with app.app_context():
        # Cria as tabelas apenas se não existirem
        db.create_all()
        # db.drop_all()

        # Verifica se a tabela 'Todo' está vazia
        if not Todo.query.first():
            # Adiciona dados iniciais
            new_todo = Todo(title="Titulo 1", complete=False)
            db.session.add(new_todo)
            db.session.commit()

    app.run(debug=True)