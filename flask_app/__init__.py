from flask import Flask
#instance of Flask class imported from flask package
app = Flask(__name__)
#secret key for session
app.secret_key = "This is my secret key"

