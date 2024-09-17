import sqlite3
from faker import Faker
import random

fake = Faker()


conn = sqlite3.connect('GO_IT_HW_2.db')
cursor = conn.cursor()


def seed_users(num_users=10):
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.email()
        try:
            cursor.execute('INSERT INTO users (fullname, email) VALUES (?, ?)', (fullname, email))
        except sqlite3.IntegrityError:
            pass


def seed_statuses():
    statuses = [('new',), ('in progress',), ('completed',)]
    cursor.executemany('INSERT OR IGNORE INTO status (name) VALUES (?)', statuses)


def seed_tasks(num_tasks=20):
    cursor.execute('SELECT id FROM users')
    user_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute('SELECT id FROM status')
    status_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(num_tasks):
        title = fake.sentence(nb_words=6)
        description = fake.text(max_nb_chars=200)
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)

        cursor.execute('''
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (?, ?, ?, ?)
        ''', (title, description, status_id, user_id))


def seed_database():
    seed_statuses()
    seed_users()
    seed_tasks()

seed_database()


conn.commit()
conn.close()

print("Database seeding completed successfully.")
