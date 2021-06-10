from flask import Flask, render_template, request, redirect, flash, session
import os,dotenv,re
from flask_pymongo import PyMongo
app = Flask(__name__)

dotenv.load_dotenv()
app.config['ENV'] = "production"
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

@app.route('/submit', methods=['POST','GET'])
def submit():
	if request.method=="POST":

		posts = mongo.db.Posts

		project_name = request.form.get("project-name")
		github_link = request.form.get("github-link")
		project_describe = request.form.get("project-describe")

		posts.insert_one({"Project_Name":project_name, "Github_Link":github_link, "Project_Description":project_describe})
		flash("Your submission has been saved!")
		return render_template("projects.html")
	return render_template("submit.html")

@app.route('/projects', methods=['GET','POST'])
def projects():
	posts=mongo.db.Posts
	project_name = posts.find({})
	return render_template('projects.html', project_name = project_name)
if __name__ == "__main__":
	app.run()