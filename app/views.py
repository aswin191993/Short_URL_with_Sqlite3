from flask import render_template, flash, redirect,request,url_for,request,session,abort
import sqlite3
import sys
import random
from flask import g
from app import app
from .forms import LoginForm
from .forms import SigninForm

@app.before_request
def before_request():
    g.db = sqlite3.connect("databook.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/',  methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = SigninForm()
	g.db.execute("CREATE TABLE IF NOT EXISTS shorturl(orginal TEXT primary key,fake TEXT)")
	name = g.db.execute("SELECT * FROM shorturl").fetchall()
	if form.validate_on_submit():
		username=form.idu.data
		try:
			log = g.db.execute("SELECT fake FROM shorturl").fetchall()
			values = "abcdefghijklmnopqrstuvwxyz"
			k="a"
			for i in xrange(0, 5):
	    			k = k+random.choice(values)			
			if k not in log:
				shorturl=(username,k) 
				g.db.execute("INSERT INTO shorturl VALUES(?,?)",shorturl)
				g.db.commit()	
        			return redirect('/index')			
			flash('Worng Username Or Password =%s' % form.idu.data)
		except sqlite3.IntegrityError:
			name = g.db.execute("SELECT * FROM shorturl").fetchall()
			for n in name:
				if n[0] == username:
					flash('Its already exist: http://127.0.0.1:5000/%s'% n[1])
		finally:
			name = g.db.execute("SELECT * FROM shorturl").fetchall()
			g.db.close()
			return render_template('index.html',form=form,name=name)
	return render_template('index.html',title='Home',form=form,name=name)


@app.route('/<msg>')
def resend(msg):
	url=msg
	try:
		name = g.db.execute("SELECT * FROM shorturl").fetchall()
		for n in name:
			if n[1] == url:
				orginal="https://"+str(n[0])
				return redirect(orginal)
	except:
		pass
	finally:
		g.db.close()
	return redirect('/index')

