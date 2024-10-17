import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="admin",  # replace with your MySQL username if different
    password="password",  # replace with your MySQL password
    database="rule_engine"
)

cursor = db.cursor()

# Fetch rules from the database
cursor.execute("SELECT * FROM rules")
rules = cursor.fetchall()
print("Rules:")
for rule in rules:
    print(rule)

# Fetch user data from the database
cursor.execute("SELECT * FROM UserData")
users = cursor.fetchall()
print("User Data:")
for user in users:
    print(user)

# Close the cursor and connection
cursor.close()
db.close()
