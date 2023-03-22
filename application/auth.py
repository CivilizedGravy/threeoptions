import sqlite3
import bcrypt

def hash(pw):
    return bcrypt.hashpw(pw,bcrypt.gensalt())
    
    
    
def auth(username,password, db):
    cur = db.cursor()
    username = username.lower()
    user = cur.execute(f'SELECT username, phash FROM users WHERE username="{username}"').fetchone()
    
    #print(user[1])
    #print(phash)
    
    if user: 
        phash = user[1]
        if bcrypt.hashpw(password, phash) == phash:
            return True
    return False
    
    
    
def add_user(username, password, email , db):
    cur = db.cursor()
    username = username.lower()
    phash = hash(password)
    user = cur.execute(f'SELECT username, phash FROM users WHERE (username="{username}")').fetchone()
    if user:
        return False
        
    cur.execute(f'INSERT INTO users(username,phash, email, templates) VALUES ("{username}", "{phash}","{email}","[]")')
    db.commit()
   
    return True
#open('data.db','w+')
con = sqlite3.connect('data.db')

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT NOT NULL UNIQUE,phash TEXT NOT NULL, email TEXT NOT NULL, templates TEXT)")
con.commit()
#t = cur.execute('SELECT username FROM users')

#t = cur.execute('SELECT phash FROM users WHERE username="earthonion"')
#cur.execute('INSERT INTO users(username, phash, templates) VALUES("earthonion",0,"[]")')

print(auth("poopbutt", "poop",con))
#print(add_user("poopbutt", 'poop', 'poop@butt.com' ,con))