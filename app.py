from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, render_template
# (rest of your code stays same)
import os

app = Flask(__name__)

# Database URL from environment variable (important for Render)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///local.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)


# Routes
@app.route("/")
def home():
    return "✅ Flask + Postgres working!"

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    todo = Todo(task=data["task"])
    db.session.add(todo)
    db.session.commit()
    return jsonify({"id": todo.id, "task": todo.task})

@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([{"id": t.id, "task": t.task} for t in todos])

@app.route("/ui")
def ui():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
