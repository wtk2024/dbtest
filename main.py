from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    value = data.get('value')

    # Save to the database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO data (name, value) VALUES (?, ?)', (name, value))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Data saved successfully!'})

@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
