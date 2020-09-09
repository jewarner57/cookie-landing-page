from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request
import jinja2

# Get DB login info from .env
load_dotenv()
db_username = os.getenv("DBNAME")
db_password = os.getenv("DBPASS")

# create flask app
app = Flask(__name__)

# create jinja loader
my_loader = jinja2.ChoiceLoader(
    [
        app.jinja_loader,
        jinja2.FileSystemLoader("data"),
    ]
)
app.jinja_loader = my_loader

# create connection with db
client = MongoClient(
    f'mongodb+srv://{db_username}:{db_password}@cluster0.ovfiw.mongodb.net/Cluster0?retryWrites=true&w=majority')

db = client["cookie_landing"]
emails_col = db["emails"]


@app.route("/")
def home():
    """Displays the homepage"""
    return render_template("home.html")


@app.route("/signup", methods=["POST"])
def signup():
    """Displays the sign up success page"""

    message = " is now subscribed"
    email = str(request.form.get("email"))

    if email_already_subscribed(email):
        message = " is already subscribed."
    else:
        subscribe_email(email)

    context = {
        'message': message,
        "email": email
    }

    return render_template("signup.html", **context)


def email_already_subscribed(email):

    search = emails_col.find_one({"email": request.form.get("email")})
    found_email = True

    if search is None:
        found_email = False

    return found_email


def subscribe_email(user_email):
    email_dict = {"email": user_email}
    emails_col.insert_one(email_dict)
    print(f"Added {user_email} to subscribers.")


"""


mydict = {"email": "jewarner57@gmail.com"}

x = mycol

print(x)"""


if __name__ == "__main__":
    app.run(debug=True)
