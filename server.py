from flask import Flask
from flask_app import app
from flask_app.controllers import login_reg_controller
from flask_app.controllers import users_controller
from flask_app.controllers import images_controller
from flask_app.controllers import comments_controller


# . Add controllers as required



# ! FOOTER OF SERVER
# < Below every route/function
# < It is ALWAYS the last lines of the file
if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=8000)

