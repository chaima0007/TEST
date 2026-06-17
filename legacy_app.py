import MySQLdb
import md5
import urllib2
import json

db = MySQLdb.connect("localhost", "root", "password123", "myapp")

def get_user(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id=" + str(id))
    return cursor.fetchone()

def login(username, password):
    cursor = db.cursor()
    hashed = md5.new(password).hexdigest()
    sql = "SELECT * FROM users WHERE username='" + username + "' AND password='" + hashed + "'"
    cursor.execute(sql)
    user = cursor.fetchone()
    if user:
        return True
    return False

def get_all_users():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = []
    for row in cursor.fetchall():
        users.append(row)
    return users

def save_user(username, password, email):
    cursor = db.cursor()
    hashed = md5.new(password).hexdigest()
    cursor.execute("INSERT INTO users (username, password, email) VALUES ('" + username + "','" + hashed + "','" + email + "')")
    db.commit()

def fetch_external_data(url):
    try:
        response = urllib2.urlopen(url)
        data = response.read()
        return json.loads(data)
    except:
        return None

def delete_user(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id=" + str(id))
    db.commit()
    print "User deleted"

def update_email(id, email):
    cursor = db.cursor()
    cursor.execute("UPDATE users SET email='" + email + "' WHERE id=" + str(id))
    db.commit()
