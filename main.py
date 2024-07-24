import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg.connect(f'dbname=postgres user={os.getenv("PG_USER")} password={os.getenv("PG_PASSWORD")} host={os.getenv("PG_HOST")} sslmode=require', row_factory=dict_row)

curr = conn.cursor()

curr.execute("""
             CREATE TABLE IF NOT EXISTS users (
                 id SERIAL PRIMARY KEY,
                 email VARCHAR NOT NULL,
                 password VARCHAR NOT NULL,
                 salt VARCHAR(12) NOT NULL DEFAULT 's',
                 first_name VARCHAR(32) NOT NULL,
                 last_name VARCHAR(32) NOT NULL,
                 role VARCHAR(20) NOT NULL DEFAULT 'student'
             )
""")

curr.execute("""
            CREATE TABLE IF NOT EXISTS classrooms (
                id SERIAL PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            )             
""")

curr.execute("""
            CREATE TABLE IF NOT EXISTS classroom_users (
                id SERIAL PRIMARY KEY,
                classroom_id INTEGER REFERENCES classrooms(id) ON DELETE CASCADE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            )        
""")

curr.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id SERIAL PRIMARY KEY,
                title VARCHAR(120) NOT NULL,
                description VARCHAR,
                due_date TIMESTAMP NOT NULL,
                classroom_id INTEGER REFERENCES classrooms(id) ON DELETE CASCADE
            )         
""")

curr.execute("""
            CREATE TABLE IF NOT EXISTS assignment_files (
                id SERIAL PRIMARY KEY,
                assignment_id INTEGER REFERENCES assignments(id) ON DELETE CASCADE,
                link VARCHAR NOT NULL
            )             
""")

curr.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id SERIAL PRIMARY KEY,
                assignment_id INTEGER REFERENCES assignments(id) ON DELETE CASCADE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                text VARCHAR
            )             
""")

curr.execute("""
            CREATE TABLE IF NOT EXISTS file_submissions (
                id SERIAL PRIMARY KEY,
                submission_id INTEGER REFERENCES submissions(id) ON DELETE CASCADE,
                link VARCHAR NOT NULL
            )             
""")

conn.commit();