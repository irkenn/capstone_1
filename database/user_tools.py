from flask import Flask, render_template, request, flash, redirect, session, g
from forms import UserAddForm, UserEditForm, UserDeleteForm
from database.models import db, connect_db, User, Thread
from sqlalchemy.exc import IntegrityError


class UserTools():
    """All the logic neccesary to aid app.py in the management of User class"""
    
    @classmethod
    def signup_handler(cls, request):
        """ For request method GET: passes the form to the user
        once the form filled (POST) creates a user, checks if there's no duplication of
        username or email, stores the user in the database and credential in the session."""
        form = UserAddForm()
        if request.method == 'POST':    
            if form.validate_on_submit():
                """Attempt to use the given info, if duplicate username/email, flash message to user informing the error"""
                try:
                    user = User.signup(form)
                    db.session.commit()
                except IntegrityError:
                    """In case there's a username or email already in use, gives a message and returns the form"""
                    db.session.rollback()
                    flash("Username or email already taken", 'danger')
                    return render_template('users/signup.html', form=form)
                """Store credentials in session and redirect to the user page"""
                session["SPOTIFY_COMMENTS_USER_KEY"] = user.id
                return redirect(f'/users/{user.id}')
        
        return render_template('users/signup.html', form=form)

    @classmethod
    def user_homepage_data(cls, url_user_id):
        """This is the user's personal page. It shows the latest threads (5 in total) from the database un a newsfeed section
         and also shows the user's activity in the page, such as threads or comments made by the user. """    
        
        latest_threads = Thread.query.order_by(Thread.timestamp.desc()).all()

        """Once the user is queried it will also contain all the threads and comments that the user has posted"""
        current_user = User.query.get_or_404(url_user_id)


        return render_template('users/user.html', user=current_user, latest_threads=latest_threads)
    
    
    @classmethod
    def other_user_homepage(cls, user_id):
        """This is the page where you can check the details about other users in the platform
        it will show all the user's activity. The difference between user's homepage is that this
        page doesn't include a newsfeed. """

        current_user = User.query.get_or_404(user_id)
        if current_user:
            return render_template('users/other-user.html', user=current_user)


    @classmethod
    def edit_user_handler(cls, request, user_id):
        """ Receives the request method, based on that passes the form to the user(GET)
        once the form filled (POST) validate the data and updates the user info.
        """
        
        user = User.query.get_or_404(session["SPOTIFY_COMMENTS_USER_KEY"])
        """Logic to send the form with the image_url field pre populated only if the user has uploaded it's own image url, otherwise it will be restored to the default argument"""
        user_image = None if user.image_url == "/static/images/default-pic.png" else user.image_url
        form = UserEditForm(username=user.username, email=user.email, image_url=user_image)
        
        if request.method == 'POST' and form.validate_on_submit():
            if User.authenticate(user.username, form.password.data):
                try:
                    user.username=form.username.data
                    user.email=form.email.data
                    user.image_url=form.image_url.data or User.image_url.default.arg
                    db.session.add(user)
                    db.session.commit()
                except IntegrityError:
                    
                    """Exception when the new username is already taken"""
                    db.session.rollback()
                    flash("New username or email is already taken", 'danger')
                    return render_template('users/edit.html', form=form, user=user)
                
                """If the operation is succesful, redirects to userpage"""
                flash("Saved changes", 'info')
                return redirect(f'/users/{user.id}')
            elif User.authenticate(user.username, form.password.data) is False:
                
                """If the password is not correct it will re send the form to confirm the info"""
                flash("Please provide the correct password", 'danger')
                return render_template('users/edit.html', form=form, user=user) #I think this line is redundant
        return render_template('users/edit.html', form=form, user=user)
    
    @classmethod
    def delete_user_handler(cls, request, user_id):
        """Receives the request method, sends a form to confirm password, 
        validates the data and deletes the user info. """

        user = User.query.get_or_404(session["SPOTIFY_COMMENTS_USER_KEY"])
        form = UserDeleteForm()
        
        if request.method == 'POST' and form.validate_on_submit():
            if User.authenticate(user.username, form.password.data) and form.confirm.data:
                db.session.delete(user)
                db.session.commit()
                flash("User deleted succesfully", 'danger')
                return redirect('/')
            
            elif User.authenticate(user.username, form.password.data) is False:
                flash("Please provide the correct password, to proceed", 'danger')
        return render_template('users/delete.html', form=form, user=user)