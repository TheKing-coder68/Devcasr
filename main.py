from flask import Flask, render_template, request, redirect, flash, session
import os,dotenv,re
from flask_pymongo import PyMongo
app = Flask(__name__)

dotenv.load_dotenv()
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', None)
mongo = PyMongo(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)

@app.route('/')
def home():
	return render_template("home.html")

@app.route('/signup', methods=['POST','GET'])
def signup():
	if request.method=="POST":
		user = mongo.db.User

		user_name = request.form.get("signup-username") 
		email = request.form.get("signup-email")
		password = request.form.get("signup-password") 

		if not re.search('^[^@ ]+@[^@ ]+\.[^@ .]{2,}$', email):
			flash("That is not a valid email entry, please try again.")

		user.insert_one({"Username":user_name, "Password":password, "Email":email})
		flash("You have signed in.")
		return render_template("signup.html")
	return render_template("signup.html")

@app.route('/login', methods=['POST','GET'])
def login():
	if request.method == "POST":
		user = mongo.db.User

		user_name= request.form.get("login-username")
		password = request.form.get("login-password")

		if not user.find_one({"Username":user_name, "Password":password}):
			flash("Your login information is incorrect, please try again.")

		if user.find_one({"Username":user_name, "Password":password}):
			flash("You have successfully logged in!!")
			return render_template("home.html")

	return render_template("login.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port='8080', debug=True)