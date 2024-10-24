# Connect to PostgreSQL using psycopg2
import os
import uuid
from datetime import datetime, timedelta

import bcrypt
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "123456")
    )

def register(username, email, password):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Hash the password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Insert new user
            cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id
            """, (username, email, password_hash.decode('utf-8')))
            
            user_id = cursor.fetchone()[0]
            conn.commit()
            print(f"User registered successfully with id: {user_id}")
            return user_id
    except (Exception, psycopg2.Error) as error:
        print(f"Error registering user: {error}")
        return None
    finally:
        conn.close()

def login(username, password):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Fetch user
            cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
                # Create session
                session_token = str(uuid.uuid4())
                expires_at = datetime.now() + timedelta(days=1)  # Session expires in 1 day
                
                cursor.execute("""
                INSERT INTO sessions (user_id, session_token, expires_at)
                VALUES (%s, %s, %s)
                """, (user[0], session_token, expires_at))
                
                conn.commit()
                print(f"User logged in successfully. Session token: {session_token}")
                return session_token
            else:
                print("Invalid username or password")
                return None
    except (Exception, psycopg2.Error) as error:
        print(f"Error logging in: {error}")
        return None
    finally:
        conn.close()

def seed():
    # Create tables for user registration and login
    conn = get_db_connection()
    print("Connected to database")
    try:
        with conn.cursor() as cursor:
            # Create users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        """)

            # Create sessions table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                session_token VARCHAR(255) UNIQUE NOT NULL,
                expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
            """)

            conn.commit()
            print("Tables created successfully")

            # Insert admin user
            admin_username = "admin"
            admin_email = "admin@example.com"
            admin_password = "admin"  # You should use a strong password in production
            admin_password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

            cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            ON CONFLICT (username) DO NOTHING
            RETURNING id
            """, (admin_username, admin_email, admin_password_hash.decode('utf-8')))

            admin_id = cursor.fetchone()
            if admin_id:
                print(f"Admin user created successfully with id: {admin_id[0]}")
            else:
                print("Admin user already exists")

            conn.commit()

    except (Exception, psycopg2.Error) as error:
        print(f"Error in database operations: {error}")

    finally:
        if conn:
            conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    seed()