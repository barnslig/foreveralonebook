#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import MySQLdb
import hashlib
import os
import random
from subprocess import Popen
from werkzeug import secure_filename
from flask import Flask, session, request, render_template, g, redirect, escape, url_for

# CONFIGURATION
SECRET_KEY = 'EJqq2cKDbGJk8M9gTLZbokf06oUAKQhOkVLmJv8fyKAfEm4WJAblcmTsfaUcfuzHglJGcHhtMzRXvbX1Bsxk9H8mOr01rovz80tlhKn0tyKCUgzepLYCx1NaEwzyYGe7umkbIs0on3TcklnFFvZ60jZLjKP2oIZMrtk74EeC2xdsFPZzwlRH40QWAR7AUJpdukGGoowmf02kMOtmFHi63zyAVbUB6DxTtUB7JoOfkA2wBh3QHZDZOVTXrfT4lSkPyx9Xqc8NnMfZemnxMzMj12Iod9j4qZ8PqzA474qNxdN8tSOCL0vMDnIrmW0FG4jFy2EtxhUhmYI6kzcUd1W5JDgpj8KxA4MTczRVBN001epYakcAfta0uOGm66tZEXbH6fwiGNRvY1ddr2TH58NKGh0gXUWfk4rzDqWD'
DEBUG = False

DB_HOST = "127.0.0.1"
DB_PORT = 3307
DB_NAME = "foreveralonebook"
DB_USER = "foreveralonebook"
DB_PWD  = "uq2XRJtq6LAw2jnr"

UPLOAD_FOLDER = 'static/avatars'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# CREATE THE APPLICATION
app = Flask(__name__)
app.config.from_object(__name__)

# function to execute something at the command line, returns the exit code
def toSystem(COMMAND):
	p = Popen(COMMAND, shell=True)
	sts = os.waitpid(p.pid, 0)[1]
	return sts
	
# function to check the uploaded file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# PAGES
@app.route("/", methods=["GET", "POST"])
def index():
	# check that there is a username in the session array which means that you are logged in
	if 'username' in session:
		
		# a post means that there is maybe a new entry
		if request.method == 'POST':
			entry = escape(request.form["entry"])
			
			# check the entry
			# no content, the entry is empty
			if len(entry) == 0:
				errormsg=u"Ein leerer Eintrag zählt nicht."
				return render_template("timeline.html", errormsg=errormsg)
				
			# correct entry
			elif len(entry) <= 170:
				g.db.cur.execute(u"INSERT INTO feabook_posts (u_id, content) VALUES ({0}, '{1}');".format(session["u_id"], entry))
				g.db.commit()
				return redirect(url_for("index"))
				
			# too long content, over 170 chars
			else:
				errormsg=u"Der Eintrag ist zu lang! Die maximal zulässige Länge liegt bei 170 Zeichen."
				return render_template("timeline.html", errormsg=errormsg)
				
		# the http method is GET, that means that the user wants to see his timeline
		else:
			# get the entries from the database
			g.db.cur.execute("SELECT content, datetime FROM feabook_posts WHERE u_id = {0} ORDER BY id DESC;".format(session["u_id"]))
			entries = [dict(content=row[0], datetime=row[1]) for row in g.db.cur.fetchall()]
			
			return render_template("timeline.html", entries=entries)
			
	# ough, the user is not logged in! show him the default start page.
	else:
		return render_template("startpage.html")
		
@app.route("/settings", methods=["GET", "POST"])
def settings():
	# check that there is a username in the session array which means that you are logged in
	if 'username' in session:
		message = ""
		# a http POST means that there is maybe a login request
		if request.method == 'POST':
			# the user has uploaded a new avatar
			if request.files["avatar_upl"]:
				file = request.files["avatar_upl"]
				# check for an allowed ending
				if file and allowed_file(file.filename):
					ending = file.filename.split(".")
					ending = ending[len(ending)-1]
					filename = "{0}.{1}".format(session["username"], ending)
					filepath = os.path.join("/tmp/feab", filename)
					endpath = os.path.join(UPLOAD_FOLDER, "{0}.png".format(session["username"]))
					file.save(filepath)
					
					# try to resize the image
					resize = toSystem("convert -resize 150x150 '{0}' '{1}'".format(filepath, endpath))
					# resize successfull
					if resize == 0:
						# remove the temporary upload
						os.remove(filepath)
						message += u"Avatar erfolgreich hochgeladen! "
					# resize not successfull -> not an image!
					else:
						message += u"Du Arsch, das ist kein richtiges Bild! "
					
			# the user has set a new password
			if request.form["new_pw"]:
				# check that the 2 passwords are the same
				if request.form["new_pw"] == request.form["new_pw_re"]:
					# make a sha1 hash of the new password
					password = hashlib.sha1(request.form["new_pw"]).hexdigest()
					# set the new password in the database
					g.db.cur.execute("UPDATE feabook_user SET password = '{0}' WHERE id = '{1}';".format(password, session["u_id"]))
					g.db.commit()
					message += u"Dein Passwort wurde erfolgreich geändert."
				else:
					message += u"Die Passwörter stimmen nicht überein. "
			# the user wants to delete
			if request.form["delete_prof"]:
				# check it
				if request.form["delete_prof"] == str(session["del_code"]):
					# delete everything from the user
					# the avatar
					os.remove("static/avatars/{0}.png".format(session["username"]))
					# the posts
					g.db.cur.execute("DELETE FROM feabook_posts WHERE u_id = {0};".format(session["u_id"]))
					# the profile
					g.db.cur.execute("DELETE FROM feabook_user WHERE id = {0};".format(session["u_id"]))
					g.db.commit()
					# the session
					session.pop("username", None)
					session.pop("u_id", None)
					session.pop("del_code", None)
					# redirect to the start page
					return redirect(url_for("index"))
				# wrong delete-code
				else:
					message += u"Der Löschcode ist falsch!"
					
		return render_template("settings.html",message=message)
	
@app.route("/register", methods=["GET", "POST"])
def register():
	# check that there is no username in the session array which means that you are not logged in
	if 'username' not in session:
		# if there is a post, there is a register request
		if request.method == "POST":			
			# make the form dingses
			username = escape(request.form["username"])
			password = hashlib.sha1(request.form["password"]).hexdigest()
			password_re = hashlib.sha1(request.form["password_re"]).hexdigest()
			# check the passwords
			if password == password_re:
				# check for this user
				g.db.cur.execute("SELECT username FROM feabook_user WHERE username = '{0}';".format(username))
				rows = g.db.cur.fetchall()
				try:
					if rows[0][0] == username:
						pass
				except IndexError:
					# create the new user
					g.db.cur.execute("INSERT INTO feabook_user (username, password) VALUES ('{0}', '{1}');".format(username, password))
					g.db.commit()
					# copy the default avatar
					toSystem("cp default-avatar.png 'static/avatars/{0}.png'".format(username))
					# log-in the new user
					g.db.cur.execute("SELECT id, username FROM feabook_user WHERE username = '{0}';".format(username))
					rows = g.db.cur.fetchall()
					session["username"] = username
					session["u_id"] = rows[0][0]
					session["del_code"] = random.randrange(1000,9999)
					# redirect him to the startpage
					return redirect(url_for("index"))
			# passwords do not compare
			else:
				message = u"Die Passwörter stimmen nicht überein."
				return render_template("register.html", message=message)
		# get request
		else:
			return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	# check that there is no username in the session array which means that you are not logged in
	if 'username' not in session:
		# a http POST means that there is maybe a login request
		if request.method == 'POST':
			status = ""
			
			# escape the username and make a sha1 sum from the password
			username = escape(request.form["username"])
			password = hashlib.sha1(request.form["password"]).hexdigest()
			
			# look in the database for the combination
			g.db.cur.execute("SELECT id, username, password FROM feabook_user WHERE username = '{0}' AND password = '{1}';".format(username, password))
			rows = g.db.cur.fetchall()
			
			# check the username
			try:
				if rows[0][1] == username:
					pass
			except IndexError:
				status = "Falscher Benutzername!"

			# check the password
			try:
				if rows[0][2] != password:
					pass
			except IndexError:
				if len(status) > 1:
					status = "Falscher Benutzername und falsches Passwort!"
				else:
					status = "Falsches Passwort!"
				
			# look for error messages
			if len(status) > 1:
				return render_template("login.html", message=status)
			# set the session if all is good
			else:
				session["username"] = username
				session["u_id"] = rows[0][0]
				session["del_code"] = random.randrange(1000,9999)
				return redirect(url_for("index"))
		else:
			return render_template("login.html")
	else:
		return redirect(url_for("index"))

@app.route("/logout")
def logout():
	session.pop("username", None)
	session.pop("u_id", None)
	session.pop("del_code", None)
	return redirect(url_for("login"))

# APP
@app.before_request
def before_request():
	g.db = connect_db()
	g.db.cur = g.db.cursor()

@app.after_request
def after_request(response):
	g.db.cur.close()
	g.db.close()
	return response

# DATABASE FUNCTIONS
def connect_db():
	#return sqlite3.connect(app.config['DATABASE'])
	return MySQLdb.connect (host = app.config["DB_HOST"],
				port = app.config["DB_PORT"],
				user = app.config["DB_USER"],
				passwd = app.config["DB_PWD"],
				db = app.config["DB_NAME"])

# START THE APPLICATION
if __name__ == "__main__":
	
	# add a global variable to the jinja template-engine: the menu
	#app.jinja_env.globals.update(
	#	menu = "hallo welt"
	#)
	
	# run the app
	app.run(host="0.0.0.0")
