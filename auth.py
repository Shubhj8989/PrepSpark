import bcrypt
import mysql.connector
from db import get_connection

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def create_user(username, password, name):
    conn = get_connection()
    cursor = conn.cursor()
    
    hashed_pw = hash_password(password).decode('utf-8') 
    
    try:
        query = "INSERT INTO users (username, password_hash, name) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, hashed_pw, name))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(user['password_hash'], password):
        return user
    return None
