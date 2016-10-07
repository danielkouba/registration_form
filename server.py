from flask import Flask, request, redirect, render_template, flash, session
import re
app = Flask(__name__)

app.secret_key = "DontLookAtMyPassword"

#something@something.something
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#Minimum 8 characters at least 1 Uppercase Alphabet, 1 Lowercase Alphabet and 1 Number:
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')




@app.route('/')
def index():
	if not 'firstname' in session:
		session['firstname'] = ""
		session['lastname'] = ""
		session['email'] = ""
		session['password'] = ""
		session['confirmpassword'] = ""
	return render_template("index.html")

@app.route('/submitted')
def submitted():
	return render_template('submitted.html', passwordstars = "*"*len(session["password"]))

@app.route('/process', methods=(['POST']))
def process():
	isEverythingValid = True
	#Firstname Check
	if len(request.form['firstname']) < 1:
		flash( "WHOOPS! Firstname cannot be empty",'firstname')
		isEverythingValid = False
	elif not request.form['firstname'].isalpha():
		flash( "WHOOPS! Firstname cannot contain numbers or special characters",'firstname')
		isEverythingValid = False
	else:
		session['firstname'] = request.form['firstname']
	
	#Lastname Check
	if len(request.form['lastname']) < 1:
		flash( "WHOOPS! Lastname cannot be empty",'lastname')
		isEverythingValid = False
	elif not request.form['lastname'].isalpha():
		flash( "WHOOPS! Lastname cannot contain numbers or special characters",'lastname')
		isEverythingValid = False
	else:
		session['lastname'] = request.form['lastname']

	#Email Check
	if len(request.form['email']) < 1:
		flash( "WHOOPS! Email cannot be empty",'email')
		isEverythingValid = False
	elif not EMAIL_REGEX.match(request.form['email']):
		flash( "WHOOPS! Email address is not valid",'email')
		isEverythingValid = False
	else:
		session['email'] = request.form['email']

	#Password Check
	if len(request.form['password']) < 8:
		flash("Password must be at least 8 characters.",'email')
		isEverythingValid = False
	elif request.form['password'] != request.form['confirmpassword']:
		flash( "WHOOPS! Passwords do not match",'email')
		isEverythingValid = False
	elif not PASSWORD_REGEX.match(request.form['password']):
		flash( "WHOOPS! Password needs at least 1 Capital 1 Lowercase and one special character",'email')
		isEverythingValid = False
	else:
		session['password'] = request.form['password']
		session['confirmpassword'] = request.form['confirmpassword']
	
	if isEverythingValid:
		return redirect('/submitted')	
	else:
		return redirect('/')
	#else go forward to submitted results
	
app.run(debug=True)