import os
import uuid
from datetime import datetime, timedelta

import bcrypt
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class Database:
    @staticmethod
    def get_db_connection():
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "123456")
        )

    @staticmethod
    def get_user(username):
        with Database.get_db_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("""
                    SELECT id, username, email, password_hash
                    FROM users
                    WHERE username = %s
                    """, (username,))
                    user = cursor.fetchone()
                    if user:
                        return {
                            "id": user[0],
                            "username": user[1],
                            "email": user[2],
                            "password": user[3]
                        }
                    return None
                except (Exception, psycopg2.Error) as error:
                    print(f"Error fetching user: {error}")
                    return None

    @staticmethod
    def create_user(username, email, password):
        with Database.get_db_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute("""
                    INSERT INTO users (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """, (username, email, hashed_password.decode('utf-8')))
                    user_id = cursor.fetchone()[0]
                    conn.commit()
                    print(f"User created successfully with id: {user_id}")
                    return user_id
                except (Exception, psycopg2.Error) as error:
                    print(f"Error creating user: {error}")
                    conn.rollback()
                    return None

    @staticmethod
    def update_user(user_id, username=None, email=None, password=None):
        with Database.get_db_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    update_fields = []
                    update_values = []

                    if username:
                        update_fields.append("username = %s")
                        update_values.append(username)
                    if email:
                        update_fields.append("email = %s")
                        update_values.append(email)
                    if password:
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        update_fields.append("password_hash = %s")
                        update_values.append(hashed_password.decode('utf-8'))

                    if not update_fields:
                        print("No fields to update")
                        return False

                    update_query = f"""
                    UPDATE users
                    SET {', '.join(update_fields)}
                    WHERE id = %s
                    """
                    update_values.append(user_id)

                    cursor.execute(update_query, tuple(update_values))
                    conn.commit()
                    print(f"User updated successfully with id: {user_id}")
                    return True
                except (Exception, psycopg2.Error) as error:
                    print(f"Error updating user: {error}")
                    conn.rollback()
                    return False