from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///course.db"
db=SQLAlchemy(app)

class Course(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

with app.app_context():
    db.create_all()
    if not Course.query.first():
        db.session.add(Course(name="Python")); db.session.commit()

# Task 1: Decompose the Monolith into Services

@app.get("/api/courses/<int:id>")
def get_course(id):
    c=Course.query.get(id)
    return (jsonify({"id":c.id,"name":c.name}),200) if c else (jsonify({"message":"Course not found"}),404)

app.run(port=5001)