from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST"),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        database=os.environ.get("MYSQL_DATABASE")
    )

# Validation
def validate_student(data):
    if not data.get("name"):
        return "Name is required"
    if not data.get("email"):
        return "Email is required"
    if not isinstance(data.get("age"), int):
        return "Age must be integer"
    return None

# CREATE
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()

    error = validate_student(data)
    if error:
        return jsonify({"error": error}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO student (name, email, age) VALUES (%s, %s, %s)"
    cursor.execute(query, (data['name'], data['email'], data['age']))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Student added"}), 201

# READ
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM student")
    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(students)

# UPDATE
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "UPDATE student SET name=%s, email=%s, age=%s WHERE id=%s"
    cursor.execute(query, (data['name'], data['email'], data['age'], id))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Student updated"})

# DELETE
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM student WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Student deleted"})

# RUN APP
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))