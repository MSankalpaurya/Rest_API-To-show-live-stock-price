from flask import Blueprint, render_template, request, redirect, flash
from flask_jwt_extended import create_access_token

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route("/", methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST':
        form_type = request.form['form_type']
        username = request.form['username']
        password = request.form['password']

        if form_type == 'login':
            try:
                # Implement your authentication logic here
                # Verify the credentials against the database
                # If authentication is successful, generate a JWT token

                # Example authentication logic:
                if username == 'abc' and password == '1234':
                    access_token = create_access_token(identity=username)
                    flash("Authentication successful.", "success")
                    return redirect("/home")
                else:
                    flash("Invalid username or password.", "error")
                    return redirect("/")
            except Exception as error:
                flash("Failed to authenticate. Error: {}".format(error), "error")
                return redirect("/")

        elif form_type == 'register':
            try:
                # Implement your registration logic here
                # Save the user to the database
                # Show an alert and redirect to the home page upon successful registration

                flash("User saved successfully.", "success")
                return redirect("/home")
            except Exception as error:
                flash("Failed to register. Error: {}".format(error), "error")
                return redirect("/")

    return render_template('login.html')
