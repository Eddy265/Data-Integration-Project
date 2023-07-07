# USER DATA MIGRATION

Description:
This project aims to unify user data across multiple databases, namely test_db and dev_db, by merging user data into a single database, merged_users. The script is written in Python and utilizes the psycopg2 library for connecting to the databases. The TimescaleDB and the Ubuntu operating system are running on Docker containers. Ensure that these components are set up and configured correctly for the migration script to function properly.

The migration script handles the migration of user data from test_db and dev_db into merged_users while considering potential duplicate users with different passwords. It ensures that the merged_users database contains the most up-to-date password for each user by comparing the passwords and their respective timestamps of change.

The script establishes connections to the source databases (test_db and dev_db) and the target database (merged_users). It retrieves user records from each source database and iterates through them. If a user exists in the merged_users database, and their password is different from the one in the source database, the script checks the timestamp of the password change. The password with the latest change time is updated in the merged_users database.

If a user is not found in the merged_users database, the script inserts their user record, including user_id, username, password, and password_last_changed, into the merged_users table.

The project ensures data consistency and a unified user management system across the databases. By executing the migration script, duplicate users with different passwords are handled appropriately, and the merged_users database reflects the most recent password changes.

Dependencies:

Python 3.x
psycopg2 library

Additional Information:
The project assumes that the TimescaleDB container and the Ubuntu operating system are running on the Docker container. Ensure that these components are set up and configured correctly for the migration script to function properly.
Usage:

Set up the necessary database connections and configurations in the script.
Execute the script to perform the migration process.
