from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, Optional, AnyOf, InputRequired
from aatool.models import User, Questiontypetwo
from aatool.helper import questionList


class RegistrationForm(FlaskForm):
    username = StringField(
        label = 'Username', 
        validators = [DataRequired(), 
        Regexp('^[a-zA-Z0-9]{2,8}$', message='Username (ID) limited to 2-8 characters long, alphanumeric only.')])
    email = StringField(
        label = 'Email', 
        validators = [DataRequired(), Email()])
    firstname = StringField(
        label = 'First Name', 
        validators = [DataRequired(), Length(max=15)])
    surname = StringField(
        label='Surname', 
        validators=[DataRequired(), Length(max=15)])
    password = PasswordField(
        label = 'Password',
        validators = [DataRequired(), Regexp('^.{6,20}$', message='Passwords limited to 6-20 characters long.')])
    confirm_password = PasswordField(
        label = 'Confirm Password', 
        validators=[DataRequired(), EqualTo('password', message='Passwords do not match.')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken. Choose another.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address is already associated with an account.')

class LoginForm(FlaskForm):
    username = StringField('Username/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class QuestionTypeOneForm(FlaskForm):
    question_id = StringField()
    question = StringField(label='Question', validators=[DataRequired()])
    option1 = StringField(label='Option 1', validators=[DataRequired()])
    option2 = StringField(label='Option 2', validators=[DataRequired()])
    option3 = StringField(label='Option 3', validators=[DataRequired()])
    option4 = StringField(label='Option 4', validators=[DataRequired()])
    answer = SelectField(
        'Answer', choices=[('1', 'Option 1'), ('2', 'Option 2'),('3','Option 3'),('4','Option 4')])
    submit = SubmitField(label='Add question')

class QuestionType2Form(FlaskForm):
    title = StringField(
        label='Title/Reference:', 
        validators=[DataRequired(message='Cannot be blank')])
    text = TextAreaField(
        label='Main question text:', 
        validators=[DataRequired(message='Field cannot be blank')])
    answer = SelectField(
        label='Correct answer: ', 
        choices=[(1, 'True'), (0, 'False')], 
        validators=[InputRequired(message='Input needed')])
    difficulty = SelectField(
        label='Difficulty: ', 
        choices=['Easy', 'Medium', 'Hard'], 
        validators=[AnyOf(['Easy', 'Medium', 'Hard'], message='Valid inputs: easy, medium, hard.')])
    feedback = TextAreaField(
        label='Feedback:', 
        validators=[Optional()])
    feedfwd = TextAreaField(
        label='Feedforward:', 
        validators=[Optional()])

#Class for checkboxes
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

#Form to add questions to assessments on makeassess section
class TestForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(max=30)] )
    files = [(x, x) for x in questionList]
    chooseQuestions = MultiCheckboxField('Choose Questions', choices = files)
    submit = SubmitField('Submit')
