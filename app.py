from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sn} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html',allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'


@app.route('/update')
def update():
    allTodo = Todo.query.all()
    print(allTodo)
    
@app.route('/delete/<int:sn>')
def delete(sn):
    # Fetch the Todo with the correct primary key
    todo = Todo.query.filter_by(sn=sn).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")
    else:
        return f"Todo with id {sn} does not exist", 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # This will create the database and tables
    app.run(debug=True, port=3000)
