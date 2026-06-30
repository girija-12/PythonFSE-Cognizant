from flask import Flask,request,Response
import requests

app=Flask(__name__)

@app.route("/api/courses/<path:path>",methods=["GET","POST","PUT","DELETE"])
def course_proxy(path):
    r=requests.request(request.method,f"http://localhost:5001/api/courses/{path}",json=request.get_json(silent=True))
    return Response(r.content,r.status_code,r.headers.items())

@app.route("/api/students/<path:path>",methods=["GET","POST","PUT","DELETE"])
def student_proxy(path):
    r=requests.request(request.method,f"http://localhost:5002/api/students/{path}",json=request.get_json(silent=True))
    return Response(r.content,r.status_code,r.headers.items())

app.run(port=5000)