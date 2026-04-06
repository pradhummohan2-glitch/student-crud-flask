from flask import Flask, request, jsonify
import os

app = Flask(__name__)

students = []
current_id = 1

# Validation
def validate_student(data):
    if not data.get("name"):
        return "Name is required"
    if not data.get("email"):
        return "Email is required"
    if not isinstance(data.get("age"), int):
        return "Age must be integer"
    return None

# Home route
@app.route('/')
def home():
    return "Student CRUD API is running 🚀"

# CREATE
@app.route('/students', methods=['POST'])
def create_student():
    global current_id
    data = request.get_json()

    error = validate_student(data)
    if error:
        return jsonify({"error": error}), 400

    data['id'] = current_id
    current_id += 1
    students.append(data)

    return jsonify(data), 201

# READ
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# UPDATE
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    for s in students:
        if s['id'] == id:
            s.update(request.get_json())
            return jsonify(s)
    return {"error": "Not found"}, 404

# DELETE
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    global students
    students = [s for s in students if s['id'] != id]
    return {"message": "Deleted"}

# RUN
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))