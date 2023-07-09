import psycopg2

# Connect to the test_db, dev_db, and merged_users databases
test_db_conn = psycopg2.connect(dbname='test_db', user='postgres', password='MYPASSWORD', host='hostname')
dev_db_conn = psycopg2.connect(dbname='dev_db', user='postgres', password='MYPASSWORD', host='hostname')
merged_users_conn = psycopg2.connect(dbname='merged_users', user='postgres', password='MYPASSWORD', host='hostname')

# Create cursors for all databases
test_db_cursor = test_db_conn.cursor()
dev_db_cursor = dev_db_conn.cursor()
merged_users_cursor = merged_users_conn.cursor()

# Retrieve user records from test_db
test_db_cursor.execute("SELECT * FROM users")
test_users = test_db_cursor.fetchall()

# Retrieve user records from dev_db
dev_db_cursor.execute("SELECT * FROM users")
dev_users = dev_db_cursor.fetchall()

# Merge user data into merged_users
for test_user in test_users:
    merged_users_cursor.execute("SELECT * FROM users WHERE username = %s", (test_user[1],))
    merged_user = merged_users_cursor.fetchone()
    if merged_user:
        if merged_user[2] != test_user[2]:
            if merged_user[3] < test_user[3]:
                merged_users_cursor.execute(
                    "UPDATE users SET password = %s, password_last_changed = %s WHERE username = %s",
                    (test_user[2], test_user[3], test_user[1])
                )
    else:
        merged_users_cursor.execute(
            "INSERT INTO users (user_id, username, password, password_last_changed) VALUES (%s, %s, %s, %s)",
            (test_user[0], test_user[1], test_user[2], test_user[3])
        )

for dev_user in dev_users:
    merged_users_cursor.execute("SELECT * FROM users WHERE username = %s", (dev_user[1],))
    merged_user = merged_users_cursor.fetchone()
    if merged_user:
        if merged_user[2] != dev_user[2]:
            if merged_user[3] < dev_user[3]:
                merged_users_cursor.execute(
                    "UPDATE users SET password = %s, password_last_changed = %s WHERE username = %s",
                    (dev_user[2], dev_user[3], dev_user[1])
                )
    else:
        merged_users_cursor.execute(
            "INSERT INTO users (user_id, username, password, password_last_changed) VALUES (%s, %s, %s, %s)",
            (dev_user[0], dev_user[1], dev_user[2], dev_user[3])
        )


# Commit the changes and close cursors
merged_users_conn.commit()
test_db_cursor.close()
dev_db_cursor.close()
merged_users_cursor.close()

# Close database connections
test_db_conn.close()
dev_db_conn.close()
merged_users_conn.close()

