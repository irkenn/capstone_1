from flask import Flask, render_template, flash, redirect, session
from database.models import User
from forms import LoginForm

class AppTools():
    """All the logic neccesary to aid app.py in the management of the State"""

    @classmethod
    def already_login(cls, g_user):
        """Flashes a info message and redirects to user its homepage"""
        flash(f"You are already logged in as {g_user.username}", 'info')
        return redirect(f'/users/{g_user.id}')

    @classmethod
    def login_handler(cls, request):
        """ Receives the request method, based on that passes the form to the user(GET)
        once the form filled (POST) validate the data and add the credentials to the session.
        """
        form = LoginForm()
        if request.method == 'POST' and form.validate_on_submit():
            user = User.authenticate(form.username.data, form.password.data)
            if user:
                """Store credentials and redirect to the user page"""
                session["SPOTIFY_COMMENTS_USER_KEY"] = user.id
                return redirect(f'/users/{user.id}')
            else:
                flash("Invalid username or password, please try again", 'danger')
                render_template('users/login.html', form=form)
        return render_template('users/login.html', form=form)
    
    @classmethod
    def do_logout(cls):
        """Logout user."""
        if "SPOTIFY_COMMENTS_USER_KEY" in session:
            del session["SPOTIFY_COMMENTS_USER_KEY"]
            flash("Log out succesful!", 'info')
            return redirect ('/login')
        return redirect('/')
        

    

        