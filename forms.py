from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, IntegerField, TextField

from wtforms.validators import DataRequired, Email, Length, Optional, URL, NumberRange

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    image_url = StringField('(Optional) Image URL', validators=[Optional(), URL(require_tld=True, message='Please provide a valid URL address or leave the field empty')])

class LoginForm(FlaskForm):
    """Form for loggin the user"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class UserEditForm(FlaskForm):
    """Form to edit the user"""

    username = StringField('Username', validators=[Optional()])
    email = StringField('E-mail', validators=[Optional(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    image_url = StringField('(Optional) Image URL', validators=[Optional(), URL(require_tld=True, message='Please provide a valid URL address or leave the field empty')])

class UserDeleteForm(FlaskForm):
    """Confirms that the user is being deleted from the database"""

    confirm = BooleanField('Delete my account and all its data', validators=[DataRequired()])
    password = PasswordField('Type your password', validators=[DataRequired(), Length(min=6)])




class AddThreadForm(FlaskForm):
    """Form to start a thread """

    title = StringField('Write your title here', validators=[DataRequired(), Length(max=130, message='Write your title in less than 130 characters')])
    description = TextField('Use this place to explain more if you need', validators=[Optional(), Length(max=500, message='Write your description in less than 500 characters')])

class SearchDatabaseForm(FlaskForm):
    """Form to search keywords in the database. """

    keyword = StringField("Type here what you're looking for", validators=[DataRequired(), Length(max=25, message='your keyword search has to be less than 25 characters')])
    
class SearchSpotifyForm(FlaskForm):
    """Form to search through Spotify's API"""

    item_type = SelectField('What kind of item are you looking for...', choices=[('album', 'Album'),('artist', 'Artist'), ('track', 'Track'), ('genre', 'Genre')], validators=[DataRequired()])
    keywords = StringField("Type here your keyword", validators=[DataRequired()])
    limit = IntegerField("Choose the amount of results", default=5, validators=[Optional(), NumberRange(min=1, max=50, message='The max number should not exeed 50') ])