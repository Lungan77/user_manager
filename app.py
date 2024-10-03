from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

def connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Lungan@7@7',
            database='user_management_system'
        )
        print('Database connected')
        return conn
    except mysql.connector.Error as error:
        print(f'Connection failed: {error}')
        return None

# Homepage
@app.route('/')
def home():
    return render_template('index.html')

# Add User Form
@app.route('/add_user_form')
def add_user_form():
    return render_template('add_user.html')

# Add User (POST)
@app.route('/add', methods=['POST'])
def add_user():
    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    registration_date = data.get('registration_date')
    
    db = connection()
    cursor = db.cursor()
    sql = 'INSERT INTO users (Username, Email, Password, Role, Registration_date) VALUES (%s, %s, %s, %s, %s)'
    values = (username, email, password, role, registration_date)

    try:
        cursor.execute(sql, values)
        db.commit()
        return redirect(url_for('list_users'))
    except mysql.connector.Error as error:
        return jsonify({"error": f"Failed to add user: {error}"}), 500
    finally:
        cursor.close()
        db.close()

# List all users
@app.route('/users')
def list_users():
    db = connection()
    cursor = db.cursor()
    sql = 'SELECT * FROM users'
    
    try:
        cursor.execute(sql)
        users = cursor.fetchall()
        return render_template('users.html', users=users)
    except mysql.connector.Error as error:
        return jsonify({"error": f"Failed to fetch users: {error}"}), 500
    finally:
        cursor.close()
        db.close()

# User Detail
@app.route('/user/<int:user_id>')
def get_user_by_id(user_id):
    db = connection()
    cursor = db.cursor()
    sql = 'SELECT * FROM users WHERE ID = %s'
    
    try:
        cursor.execute(sql, (user_id,))
        user = cursor.fetchone()
        if user:
            return render_template('user_detail.html', user=user)
        return jsonify({"message": "User not found"}), 404
    except mysql.connector.Error as error:
        return jsonify({"error": f"Failed to retrieve user: {error}"}), 500
    finally:
        cursor.close()
        db.close()

# Update User Form
@app.route('/update_user_form/<int:user_id>')
def update_user_form(user_id):
    db = connection()
    cursor = db.cursor()
    sql = 'SELECT * FROM users WHERE ID = %s'

    try:
        cursor.execute(sql, (user_id,))
        user = cursor.fetchone()
        if user:
            return render_template('update_user.html', user=user)
        return jsonify({"message": "User not found"}), 404
    except mysql.connector.Error as error:
        return jsonify({"error": f"Failed to retrieve user: {error}"}), 500
    finally:
        cursor.close()
        db.close()

# Update User (POST)
@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    db = connection()
    cursor = db.cursor()
    data = request.form

    sql = 'UPDATE users SET Username = %s, Email = %s, Password = %s, Role = %s WHERE ID = %s'
    values = (data.get('username'), data.get('email'), data.get('password'), data.get('role'), user_id)

    try:
        cursor.execute(sql, values)
        db.commit()
        return redirect(url_for('get_user_by_id', user_id=user_id))
    except mysql.connector.Error as error:
        return jsonify({"error": f"Failed to update user: {error}"}), 500
    finally:
        cursor.close()
        db.close()

# Delete User Form
@app.route('/delete_user_form/<int:user_id>')
def delete_user_form(user_id):
    return render_template('delete_user.html', user_id=user_id)

# Delete User (POST)
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    db = connection()
    cursor = db.cursor()
    sql = 'DELETE FROM users WHERE ID = %s'

    try:
        cursor.execute(sql, (user_id,))
        db.commit()
        return redirect(url_for('list_users'))
    except mysql.connector.Error as error:
        return jsonify({"error": f"Failed to delete user: {error}"}), 500
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
