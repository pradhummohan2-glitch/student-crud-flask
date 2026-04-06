
from flask import Flask, request, jsonify
from db_config import mysql, init_db

app = Flask(__name__)
init_db(app)

def validate_student(data):
    if not data.get("name"):
        return "Name is required"
    if not data.get("email"):
        return "Email is required"
    if not data.get("age"):
        return "Age is required"
    if not isinstance(data.get("age"), int):
        return "Age must be integer"
    return None

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    error = validate_student(data)
    if error:
        return jsonify({"error": error}), 400

    cursor = mysql.connection.cursor()
    query = "INSERT INTO student (name, email, age) VALUES (%s, %s, %s)"
    cursor.execute(query, (data['name'], data['email'], data['age']))
    mysql.connection.commit()

    return jsonify({"message": "Student added successfully"}), 201

@app.route('/students', methods=['GET'])
def get_students():
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()
    return jsonify(students)

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    query = "UPDATE student SET name=%s, email=%s, age=%s WHERE id=%s"
    cursor.execute(query, (data['name'], data['email'], data['age'], id))
    mysql.connection.commit()
    return jsonify({"message": "Student updated successfully"})

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM student WHERE id=%s", (id,))
    mysql.connection.commit()
    return jsonify({"message": "Student deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
