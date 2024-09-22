from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import psycopg2

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(database="paydb",
                        user="ben",
                        password="Starwars",
                        host="localhost", port="5432")

cur = conn.cursor()

cur.execute(
    '''CREATE TABLE IF NOT EXISTS users (username varchar(100) UNIQUE, password varchar(100));''')

cur.execute(
    '''INSERT INTO users (username, password) VALUES 
    ('Ben', 'Ben'), ('Henry', 'Henry'), ('Wyatt', 'Wyatt') ON CONFLICT (username) DO NOTHING;''')

conn.commit()

cur.close()
conn.close()

# Route for home (optional, just to test)
@app.route('/')
def home():
    return "Welcome to the user management system!"

@app.route('/api/users', methods=['GET'])
def get_users():
    # Connect to the database
    conn = psycopg2.connect(database="paydb",
                            user="ben",
                            password="Starwars",
                            host="localhost", port="5432")

    cur = conn.cursor()

    # Fetch all users
    cur.execute('''SELECT * FROM users''')
    users = cur.fetchall()

    # Close the connection
    cur.close()
    conn.close()

    # Return the data as JSON
    return jsonify(users)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Connect to the database
    conn = psycopg2.connect(database="paydb",
                            user="ben",
                            password="Starwars",
                            host="localhost", port="5432")
    cur = conn.cursor()

    # Query the database to check if the user exists with the given username and password
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()

    cur.close()
    conn.close()

    # If user exists, return success response, otherwise return error
    if user:
        return jsonify({'status': 'success', 'message': 'Login successful'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
