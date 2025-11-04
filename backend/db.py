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


# Function to get a connection from the pool
def get_connection():
    if connection_pool:
        return connection_pool.get_connection()
    else:
        raise ConnectionError("Database connection pool is not initialized.")


# Backwards-compatible name used in some routes
def get_db_connection():
    return get_connection()


# Utility function for executing SELECT queries
def fetch_all(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# Alias used by some existing code
def fetch_query(query, params=None):
    return fetch_all(query, params)


def fetch_one(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row



def execute_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    cursor.close()
    conn.close()
    return True


def call_procedure(proc_name, params=()):
    """Call a stored procedure without returning a result set."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc(proc_name, params)
    conn.commit()
    cursor.close()
    conn.close()
    return True
