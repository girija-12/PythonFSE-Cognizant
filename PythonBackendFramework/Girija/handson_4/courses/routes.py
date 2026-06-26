from flask import Blueprint, jsonify, request

# Task 1: Flask App Structure and Basic Routing

courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)

courses = []

next_id = 1


# Task 2: Request Handling and JSON Responses

def make_response_json(data, status_code=200):
    return jsonify({
        "status": "success",
        "data": data
    }), status_code


@courses_bp.route("/", methods=["GET"])
def get_courses():
    return make_response_json(courses)


@courses_bp.route("/", methods=["POST"])
def create_course():
    global next_id

    data = request.get_json()

    if data is None:
        return jsonify({
            "status": "error",
            "message": "Request body must be JSON."
        }), 400

    required_fields = ["name", "code", "credits"]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "status": "error",
                "message": f"Missing required field: {field}"
            }), 400

    course = {
        "id": next_id,
        "name": data["name"],
        "code": data["code"],
        "credits": data["credits"]
    }

    next_id += 1

    courses.append(course)

    return make_response_json(course, 201)


@courses_bp.route("/<int:course_id>/", methods=["GET"])
def get_course(course_id):

    for course in courses:
        if course["id"] == course_id:
            return make_response_json(course)

    return jsonify({
        "status": "error",
        "message": "Course not found"
    }), 404


@courses_bp.route("/<int:course_id>/", methods=["PUT"])
def update_course(course_id):

    data = request.get_json()

    if data is None:
        return jsonify({
            "status": "error",
            "message": "Request body must be JSON."
        }), 400

    for course in courses:

        if course["id"] == course_id:

            course["name"] = data.get("name", course["name"])
            course["code"] = data.get("code", course["code"])
            course["credits"] = data.get("credits", course["credits"])

            return make_response_json(course)

    return jsonify({
        "status": "error",
        "message": "Course not found"
    }), 404


@courses_bp.route("/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):

    for course in courses:

        if course["id"] == course_id:

            courses.remove(course)

            return make_response_json(
                {
                    "message": "Course deleted successfully."
                }
            )

    return jsonify({
        "status": "error",
        "message": "Course not found"
    }), 404