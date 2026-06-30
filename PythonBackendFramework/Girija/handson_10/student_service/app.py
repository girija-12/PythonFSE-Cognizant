from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import requests

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///student.db"
db=SQLAlchemy(app)

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

with app.app_context():
    db.create_all()
    if not Student.query.first():
        db.session.add(Student(name="John")); db.session.commit()

# Task 2: Inter-Service Communication and API Gateway Pattern

@app.post("/api/students/<int:id>/enroll")
def enroll(id):
    cid=request.json["course_id"]
    try:
        r=requests.get(f"http://localhost:5001/api/courses/{cid}")
        if r.status_code!=200: return jsonify({"message":"Course not found"}),404
    except requests.exceptions.ConnectionError:
        return jsonify({"message":"Course Service unavailable"}),503
    return jsonify({"message":"Enrollment successful","student":id,"course":cid}),200

app.run(port=5002)