from flask import Flask, request, jsonify
from datetime import datetime, timedelta

import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host = "birthday-mysql-rds-db.cnkqwsuqkmlq.eu-central-1.rds.amazonaws.com",
        user = "admin",
        password = "1234abcd",
        database = "friends"
    )
    return conn

def days_until_birthday(birthday_str):
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
    birthday = birthday.replace(year=today.year)
    
    # If the birthday has already passed this year, we use the next year
    if birthday < today:
        birthday = birthday.replace(year=today.year + 1)
    
    days_left = (birthday - today).days
    return days_left

@app.route("/health", methods = ["GET"])
def health_check():
    return "The light inside has broken but i still work", 200
"""
@app.route("/when", methods = ["POST"])
def get_next_bday():
    birthday_str = request.get_json().get("birthday")
    days_left = days_until_birthday(birthday_str)
    return jsonify({"Days until next birthday": days_left}), 200

@app.route("/when/<int:id>", methods = ["GET"])
def get_next_friend_bday(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, DATE_FORMAT(birthday, '%Y-%m-%d') AS 'birthday' FROM birthdays WHERE id = %s", (id,))
    friend = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not friend:
        return jsonify({"error": "Friend not found"}), 404
    
    birthday_str = friend.get("birthday")
    days_left = days_until_birthday(birthday_str)
    friend["Days until next birthday"] = days_left
    return jsonify(friend), 200
"""
# READ all
@app.route('/friends', methods=['GET'])
def get_friends():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, DATE_FORMAT(birthday, '%Y-%m-%d') AS 'birthday' FROM birthdays")
    friends = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(friends), 200

# READ one
@app.route('/friends/<int:id>', methods=['GET'])
def get_friend(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, DATE_FORMAT(birthday, '%Y-%m-%d') AS 'birthday' FROM birthdays WHERE id = %s", (id,))
    friend = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not friend:
        return jsonify({"error": "Friend not found"}), 404

    return jsonify(friend), 200

# CREATE
@app.route('/friends', methods=['POST'])
def add_friend():
    data = request.get_json()
    name = data.get('name')
    birthday = data.get('birthday')
    
    if not name or not birthday:
        return jsonify({"error": "Name and date of birth are required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO birthdays (name, birthday) VALUES (%s, %s)", (name, birthday))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Friend added successfully"}), 200

# UPDATE one
@app.route('/friends/<int:id>', methods=['PUT'])
def update_friend(id):
    data = request.get_json()
    name = data.get('name')
    birthday = data.get('birthday')
    
    if not name or not birthday:
        return jsonify({"error": "Name and date of birth are required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE birthdays SET name = %s, birthday = %s WHERE id = %s", (name, birthday, id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Friend updated successfully"}), 200

# DELETE one
@app.route('/friends/<int:id>', methods=['DELETE'])
def delete_friend(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM birthdays WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Friend deleted successfully"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)