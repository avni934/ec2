from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
db=SQLAlchemy(app)

class Todo(db.Model):#yahan pe database create kiya
    sno= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(200), nullable=False)
    desc= db.Column(db.String(200), nullable=False)
    date_created= db.Column(db.DateTime, default=datetime.now)

def __repr__(self)->str:
    return f"{self.sno} - {self.title}"

@app.route('/', methods=["POST","GET"])
def hello_world():
    if request.method=='POST':
        title=request.form['title']#ye form ka reponse h
        desc=request.form['desc']#ye form ka reponse h
        todo=Todo(title=title,desc=desc)#form k reponse ko database se link kiya au todo ko database bana diya
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()#all todo database ki saari rows le lega
    return render_template('index.html',allTodo=allTodo)

@app.route('/show')
def products():
    alltodo=Todo.query.all()
    return 'This is products page'

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()#query dhundh rhe h
    db.session.delete(todo)
    db.session.commit()
    return redirect ("/")

@app.route('/update/<int:sno>', methods=["POST","GET"])
def update(sno):
    if request.method=="POST":
        title=request.form['title']#ye form ka reponse h
        desc=request.form['desc']#ye form ka reponse h
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)


if __name__=="__main__":
    app.run(debug=True, port=8000)