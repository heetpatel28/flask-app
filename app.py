import os
from flask import Flask
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        # These credentials are read from Environment Variables
        conn = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST'),       # This will be 'mysql' (the service name)
            database=os.environ.get('MYSQL_DATABASE'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD')
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def initialize_db():
    """Creates the 'visits' table if it doesn't already exist."""
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed. Check logs."
    
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            count INT NOT NULL DEFAULT 0
        );
    """)
    
    # Check if a row exists, if not, insert one
    cursor.execute("SELECT COUNT(id) FROM visits")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO visits (count) VALUES (0)")
    
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def index():
    """Handles the main route, increments and displays the visit count."""
    conn = get_db_connection()
    if conn is None:
        return "<h1>Database connection failed!</h1><p>Please check the application logs.</p>", 500

    cursor = conn.cursor()
    
    # Increment the visit count
    cursor.execute("UPDATE visits SET count = count + 1 WHERE id = 1")
    conn.commit()
    
    # Fetch the new count
    cursor.execute("SELECT count FROM visits WHERE id = 1")
    count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    
    return f"<h1>CI/CD Pipeline is good!</h1><p>This page has been visited {count} times.</p>"

if __name__ == '__main__':
    initialize_db()  # Ensure the table exists before running
    app.run(host='0.0.0.0', port=5050, debug=True)