from flask import Flask, render_template, request, url_for, redirect, session, flash
import json
import os
import sqlite3
from . import app, auth
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        
def getuser(username):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    user = cur.execute(f'SELECT username, templates FROM users WHERE (username="{username}")').fetchone()
    return user
    
def update_templates(username, new_data):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    #new_data = new_data.encode('unicode_escape')
    
    print(new_data)
    user = cur.execute(f"UPDATE users SET  templates=json('{new_data}') WHERE (username='{username}')")
    con.commit()
    
@login_manager.user_loader
def load_user(user_id):
    # This function should return a User object based on the user_id passed to it.
    
    return User(user_id)

login_manager.login_view = 'login'

@app.route('/delete',methods=['GET', 'POST'] )
@login_required
def delete():
    arg = lambda x: request.args.get(x) if request.args.get(x) else ""
    username = session['user_id']
    data = json.loads(getuser(username)[1])
    
    title = arg('ptitle')
    
    data = [d for d in data if d.get('ptitle') != title]
    
    
    update_templates(username, json.dumps(data))
    return redirect(url_for('index'))
    
@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    
    arg = lambda x: request.args.get(x) if request.args.get(x) else ""
    presentation_title = arg('ptitle')
    
    title1 = arg('title1')
    title2 = arg('title2')
    title3 = arg('title3')
    
    price1 = arg('price1')
    price2 = arg('price2')
    price3 = arg('price3')
    
    monthly1 = arg('monthly1')
    monthly2= arg('monthly2')
    monthly3 = arg('monthly3')
    
    benefits1 = arg('benefits1')
    benefits2 = arg('benefits2')
    benefits3 = arg('benefits3')
	
    return render_template('index.html',ptitle = presentation_title, b1 = benefits1,b2 =benefits2, b3 = benefits3, m1 = monthly1, m2 = monthly2 ,m3 = monthly3, p1 = price1, p2 = price2 ,p3 = price3, t1 = title1, t2 = title2, t3 = title3)
	
	
@app.route('/present')
@login_required
def present():
    print(request.args.to_dict())
    arg = lambda x: request.args.get(x)
    
    presentation_title = arg('ptitle')
    
    title1 = arg('title1')
    title2 = arg('title2')
    title3 = arg('title3')
    
    price1 = arg('price1')
    price2 = arg('price2')
    price3 = arg('price3')
    
    monthly1 = arg('monthly1')
    monthly2= arg('monthly2')
    monthly3 = arg('monthly3')
    
    benefits1 = arg('benefits1').split(',')
    benefits2 = arg('benefits2').split(',')
    benefits3 = arg('benefits3').split(',')
    
    
    
    
    option1 = {'title':'Good' ,'price':15000, 'monthly' : True, 'benefits' : [  '14 SEER Heat Pump',
                                '10 year parts warranty',
                                '2 year labor warranty',
                                'Free Heroes Club Membership']}
    return render_template('present.html',b1 = benefits1,b2 =benefits2, b3 = benefits3, m1 = monthly1, m2 = monthly2 ,m3 = monthly3, p1 = price1, p2 = price2 ,p3 = price3, t1 = title1, t2 = title2, t3 = title3 )
    
    
@app.route('/saveoptions')
@login_required
#http://127.0.0.1:5000/saveoptions?ptitle={{t['ptitle']}}&title1={{t['title1']}}&price1={{t['price1']}}&benefits1={{t['benefits1']}}&title2={{t['title2']}}&price2={{t['price2']}}&benefits2={{t['benefits2']}}&title3={{t['title3']}}&price3={{t['price3']}}&benefits3={{t['benefits3']}}
def saveoptions():
    #save to user profilejson
    username = session['user_id']
    user_data = getuser(username)
    if not user_data:
        return redirect(url_for('index'))
    print(request.args.to_dict())
    arg = lambda x: request.args.get(x)
    #f = open(os.getcwd()+'/o.json', 'r')
    
    json_temps=json.loads(user_data[1])
    #f.close()
    
    json_temps.append(request.args.to_dict())
    
    #f = open(os.getcwd()+'/o.json', 'w')
    #f.write
    update_templates(username, json.dumps(json_temps, indent=4))
    #f.close()
    
    return redirect(url_for('index'))
    
@app.route('/')
@login_required
def index():
    #load user profile json
    #t = open(os.getcwd()+'/o.json', 'r')
    username=session['user_id']
    user_data= getuser(username)
    if not user_data:
        return redirect(url_for('login'))
    saved_temps = json.loads(user_data[1])
    
    return render_template('templates.html', saved_templates = saved_temps)
    
    
    
@app.route('/signup', methods = ['POST','GET'])
def signup():
    
    if request.method == 'POST':
        form = request.form
        email = form['email']
        username = form['user_id']
        pass1 = form['password']
        pass2 = form['password2']
        
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        user = cur.execute(f'SELECT username FROM users WHERE (username="{username}")').fetchone()
        #print(user[1])
        if user:
            flash('Username already exists')
        elif pass1 != pass2:
            flash('Passwords dont match')
        elif len(pass1) < 6:
            flash('Password too short')
        else:
            if auth.add_user(username,pass1,email,con):
                flash('Sign up successful!')
                return redirect(url_for('login'))
                
            else:
                flash('Something went wrong')
        return render_template('signup.html')
        #return request.form
        
    return render_template('signup.html')
    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        con = sqlite3.connect('data.db')

        # Here you can check if the user exists and their password is correct.
        
        username = request.form['user_id']
        password = request.form['password']
        user = auth.auth(username, password,con)
        if user:
            # If the user is authenticated, store their ID in the session
            session['user_id'] = username
            user = User(user_id)
            login_user(user)
            return redirect(url_for('index'))
        else:
            # utilize flasks flash function
            flash('Invalid username or password')
            return render_template('login.html')
       
       
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    logout_user()
    return redirect(url_for('index'))
    
@login_manager.unauthorized_handler
def unauthorized():
    # Redirect the user to the login page if they try to access an unauthorized view.
    return redirect(url_for('login'))
    
if __name__ == '__main__':
	app.run(debug=True)
