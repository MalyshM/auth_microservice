import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def db_create_users_table():
    conn = psycopg2.connect(
        dbname="postgres",
        user=os.getenv("DB_USER", ""),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", ""),
    )
    cursor = conn.cursor()

    conn.autocommit = True
    sql = f"""DROP DATABASE IF EXISTS {os.getenv("DB_NAME", "auth_users")};"""
    cursor.execute(sql)
    sql = f"""
    CREATE DATABASE {os.getenv("DB_NAME", "auth_users")}
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
        dbname=os.getenv("DB_NAME", ""),
        user=os.getenv("DB_USER", ""),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", ""),
    )
    cursor = conn.cursor()
    conn.autocommit = True
    sql1 = f"""
create extension if not exists "uuid-ossp";
DROP TABLE IF EXISTS {os.getenv("TABLE_NAME", "users")} CASCADE;
CREATE TABLE users (
    {os.getenv("ID_FIELD", "id")} UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    {os.getenv("USERNAME_FIELD", "username")} VARCHAR(255) UNIQUE,
    {os.getenv("PASSWORD_FIELD", "password")} VARCHAR(255) NOT NULL,
    {os.getenv("EMAIL_FIELD", "email")} VARCHAR(255) UNIQUE,
    {os.getenv("PHONE_FIELD", "phone")} VARCHAR(255) UNIQUE
);
    """
    cursor.execute(sql1)
    conn.commit()
    print("Database created successfully........")

    # Closing the connection

    cursor.close()
    conn.close()


def db_create_pkce_table():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME", ""),
        user=os.getenv("DB_USER", ""),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", ""),
    )
    cursor = conn.cursor()
    conn.autocommit = True
    sql1 = f"""
create extension if not exists "uuid-ossp";
DROP TABLE IF EXISTS pkce CASCADE;
CREATE TABLE pkce (
    {os.getenv("ID_FIELD", "id")} UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    host VARCHAR(255) UNIQUE,
    code_challenge VARCHAR(255) NOT NULL,
    code_challenge_method VARCHAR(255) NOT NULL
);
    """
    cursor.execute(sql1)
    conn.commit()
    print("PKCE database created successfully........")

    # Closing the connection

    cursor.close()
    conn.close()


db_create_users_table()
db_create_pkce_table()
