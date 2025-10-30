import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'streamingdb'),
}

try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="streaming_pool",
        pool_size=5,
        pool_reset_session=True,
        **DB_CONFIG
    )
    print("✅ MySQL connection pool created successfully.")
except mysql.connector.Error as err:
    print(f"❌ Error creating connection pool: {err}")
    connection_pool = None


def get_connection():
    """Get a connection from the pool."""
    if connection_pool:
        return connection_pool.get_connection()
    else:
        raise ConnectionError("Database connection pool is not initialized.")


def get_db_connection():
    """Backwards compatibility alias."""
    return get_connection()


def fetch_all(query, params=None):
    """Run SELECT queries safely and return list of dicts."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        print(f"❌ DB fetch error: {err}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def execute_query(query, params=None):
    """Run INSERT/UPDATE/DELETE safely."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f" DB execution error: {err}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def fetch_query(query, params=None):
    """Alias for fetch_all for consistent naming."""
    return fetch_all(query, params)
