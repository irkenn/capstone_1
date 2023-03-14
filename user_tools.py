from flask import Flask, render_template, request, flash, redirect, session, g
from forms import UserAddForm, UserEditForm
from models import db, connect_db, User
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
        

        if g.user.id == url_user_id:
            current_user = User.query.get_or_404(url_user_id)
            # print('request.args.get("q")', request.args.get('q')) # there's a search field in the page this will retrieve those arguments
                #logic to be applied to render the homepage info (too soon to deal with this right now)
                
                # ids = [u.id for u in current_user.following]
                # ids.append(g.user.id)
                # messages = (db.session.query(Message)
                #             .filter(Message.user_id.in_(ids))
                #             .order_by(Message.timestamp.desc())
                #             .limit(100)
                #             .all())
                # likes = (db.session.query(Likes.message_id)
                #         .filter(Likes.user_id == g.user.id)
                #         .all())
                # likes = [i[0] for i in likes] ## to eliminate the comma of each tuple
            return render_template('users/user.html', user=current_user)
        return redirect('/login')
    

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