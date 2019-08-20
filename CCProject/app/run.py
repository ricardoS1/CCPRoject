from flask import Flask
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flaskext.mysql import MySQL
import os

DB_HOST = os.getenv('DB_HOST', 'host')
DB_NAME = os.getenv('DB_NAME', 'name')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

app = Flask(__name__)
app.secret_key = "stairsSecret"

app.config['MYSQL_DATABASE_HOST'] = DB_HOST
app.config['MYSQL_DATABASE_USER'] = DB_USER
app.config['MYSQL_DATABASE_PASSWORD'] = DB_PASSWORD
app.config['MYSQL_DATABASE_DB'] = DB_NAME


mysql = MySQL()
mysql.init_app(app)



@app.route('/status')
def health_check():
    return 'Running!'

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods = ['POST','GET'])
def login():
    if(request.method == "POST"):
        email = request.form['email']
        password = request.form['password']
        
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email= %s",(email))
        user = cur.fetchone()
        cur.execute("SELECT * FROM subscriptions WHERE EMAIL= %s AND CURRENT_SUB != 1", (email))
        subscriptions = cur.fetchall()
        cur.execute("SELECT * FROM subscriptions WHERE EMAIL= %s AND CURRENT_SUB = 1", (email))
        current_sub = cur.fetchone()
        #print("SUBSCRIPTION: ",subscription)
        cur.close()

        if(len(user) > 0):
            print('Password from form: ',password)
            print(' Password from db: ',user[4])
            if(password == user[4]):
                #for user information on profile page
                session['name'] = user[1]
                session['surname'] = user[2]
                session['email'] = user[3]
                session['phone'] = user[5]
                session['address'] = user[6]
                session['organization'] = user[7]
                session['package'] = user[8]
                session['cc_number'] = user[9]

                #for subscription info on profile page
                session['subscriptions'] = subscriptions
                session['current_sub'] = current_sub






                return redirect(url_for('homepage'))
    return render_template('login.html')

@app.route('/profile', methods = ['POST','GET'])
def profile():
    if request.method == 'GET':
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email= %s",(session['email']))
        user = cur.fetchone()
        print("USER INFO: ls",user)
        cur.close()
        return render_template('profile.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))

@app.route('/subscriptions')
def subscriptions():
    return render_template('subscriptions.html')

@app.route('/update_sub', methods = ['POST'])
def update_subscription():
    if request.method == 'POST':
        package = request.form['package']

        conn = mysql.connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM subscriptions WHERE EMAIL= %s AND CURRENT_SUB = 1", (session['email']))
        current_sub = cur.fetchone()


        #nothing has changed
        if(current_sub[2] == package):
            cur.close()
            return render_template('profile.html')
        else:

            cur.execute('UPDATE subscriptions SET D_UNSUBSCRIBED = CURRENT_TIMESTAMP, CURRENT_SUB = 0 WHERE EMAIL= %s '
                        'AND CURRENT_SUB = 1;',(session['email']))
            cur.execute('INSERT INTO subscriptions (EMAIL,CURRENT_SUB, PACKAGE) VALUES ( %s, %s, %s)',
                        (current_sub[0], 1, package))
            cur.execute("SELECT * FROM subscriptions WHERE EMAIL= %s AND CURRENT_SUB != 1", (session['email']))
            subscriptions = cur.fetchall()
            cur.execute("SELECT * FROM subscriptions WHERE EMAIL= %s AND CURRENT_SUB = 1", (session['email']))
            current_sub = cur.fetchone()
            session['subscriptions'] = subscriptions
            session['current_sub'] = current_sub

            conn.commit()


            return render_template('profile.html')






@app.route('/registration', methods = ['POST','GET'])
def register():
    return render_template('registration.html')

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        flash("Data Inserted Successfully.")
        first_name = request.form['first_name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        # hash_password = bcrypt.hashpw(password, bcrypt.gensalt)

        # salt = uuid.uuid4().hex
        # password = hashlib.sha512(password + salt).hexdigest()

        phone = request.form['phone']
        address = request.form['address']
        organization = request.form['organization']
        package = request.form['package']
        
        cc_number = request.form['cc_number']
        cc_pin = request.form['cc_pin']
        
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (FIRST_NAME, SURNAME, EMAIL , PASSWORD, PHONE, ADDRESS, ORGANIZATION, PACKAGE, CC_NUMBER, CC_PIN) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (first_name, surname, email, password, phone, address, organization, package, cc_number, cc_pin  )) 
        
        if(package == 'Free'):
            cur.execute('INSERT INTO subscriptions (EMAIL,CURRENT_SUB, PACKAGE) VALUES ( %s, %s, %s)',
                        (email, 1, 'Free'))
            # cur.execute('INSERT INTO user_services (UID, CURRENT_SUBSCRIPTION, P_FREE) VALUES ( %s, %s, %s)',
            #         (email, package, 'Yes'))
        elif(package == 'Standard'):
            cur.execute('INSERT INTO subscriptions (EMAIL,CURRENT_SUB, PACKAGE) VALUES ( %s, %s, %s)',
                        (email, 1, 'Standard'))
        elif(package == 'Enterprise'):
            cur.execute('INSERT INTO subscriptions (EMAIL,CURRENT_SUB, PACKAGE) VALUES ( %s, %s, %s)',
                        (email, 1, 'Enterprise'))
        else:
            cur.execute('INSERT INTO subscriptions (EMAIL) VALUES ( %s)',
                    (email))

    
        # session['name'] = first_name
        # session['surname'] = surname
        # session['email'] = email
        # session['phone'] = phone
        # session['address'] = address
        # session['organization'] = organization
        # session['package'] = package
        # session['cc_number'] = cc_number
        
        conn.commit()
        cur.close()
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)




# from flask import Flask
# from flask import Flask, render_template, redirect, request, url_for, flash
# from flaskext.mysql import MySQL

# app = Flask(__name__)

# @app.route('/status')
# def health_check():
#     return 'Running!'

# @app.route('/')
# def homepage():
#     return render_template('homepage.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

# @app.route('/subscriptions')
# def subscriptions():
#     return render_template('subscriptions.html')

# @app.route('/registration')
# def register():
#     return render_template('registration.html')

# if __name__ == "__main__":
# 	app.run("0.0.0.0", 5000, debug=True)
