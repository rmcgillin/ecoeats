import sqlite3

# Establish connection to database
conn = sqlite3.connect('EcoEats Database.db')
cursor = conn.cursor()

forename = input("Enter your forename: ")
surname = input("Enter your surname: ")
email = input("Enter your email address: ")
password = input("Enter your password: ")
phone_number = input("Enter your phone number:")

# SQL query to insert a new user into the "users" table
insert_query = """
INSERT INTO users (forename, surname, email, password, phone_number)
VALUES (?, ?, ?, ?, ?)
"""

# Execute the query with user information as parameters
cursor.execute(insert_query, (forename, surname, email, password, phone_number))


# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()

