import psycopg2


def db_create_users_table():
    conn = psycopg2.connect(
        dbname="postgres", user="postgres", password="admin", host="localhost"
    )
    cursor = conn.cursor()

    conn.autocommit = True
    sql = """DROP DATABASE IF EXISTS auth_users;"""
    cursor.execute(sql)
    sql = """
    CREATE DATABASE auth_users
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
    """
    try:
        cursor.execute(sql)
    except psycopg2.Error as e:
        print("Error creating database:", e)
    conn.commit()
    cursor.close()
    conn.close()
    conn = psycopg2.connect(
        dbname="auth_users", user="postgres", password="admin", host="localhost"
    )
    cursor = conn.cursor()
    conn.autocommit = True
    sql1 = """
create extension if not exists "uuid-ossp";
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    id UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(255) UNIQUE
);
    """
    cursor.execute(sql1)
    conn.commit()
    print("Database created successfully........")

    # Closing the connection

    cursor.close()
    conn.close()


db_create_users_table()
