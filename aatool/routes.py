from flask import render_template, url_for, request, redirect, flash
from aatool import app, db
from aatool.forms import RegistrationForm, LoginForm, QuestionTypeOneForm, QuestionType2Form, MultiCheckboxField, TestForm
from aatool.models import User, Questiontypetwo, grade_labels, test_results, grade_amounts, string_grades, colors, recent_assessment, students_taken, Question_type1, Assessment, Assessment_questionstype1,Assessment_questionstype2

from flask_login import login_user, logout_user, login_required, current_user
#https://stackoverflow.com/questions/65068073/error-while-showing-matplotlib-figure-in-flask
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv


@app.route("/")
@app.route("/home", methods=['GET','POST'])
def home():
    return render_template('home.html', title='Home')

@app.route("/type1", methods=["GET", "POST"])
def createType1():
    form = QuestionTypeOneForm()
    questions = Question_type1.query.all()
    if form.validate_on_submit():
     question = Question_type1(question_text= form.question.data,option_one= form.option1.data,option_two= form.option2.data,option_three= form.option3.data, option_four = form.option4.data, correct_answer = form.answer.data)
     db.session.add(question)
     db.session.commit()
    return render_template('type1.html', form = form,title='type1',questions = questions)


@app.route("/editType1", methods=["GET", "POST"])
def editType1():
    form = QuestionTypeOneForm()
    print(form.question_id.data)
    question = Question_type1.query.filter_by(id=form.question_id.data).first()
    print(question)
    if form.validate_on_submit():
     db.session.delete(question)
     db.session.commit()
     question = Question_type1(question_text= form.question.data,option_one= form.option1.data,option_two= form.option2.data,option_three= form.option3.data, option_four = form.option4.data, correct_answer = form.answer.data)
     db.session.add(question)
     db.session.commit()
    return redirect(url_for("createType1"))


@app.route("/getType1/<question_id>", methods=["GET","POST"])
def getType1(question_id):
    # content = request.json
    # question_id = content["question_id"]
    print("question_id",question_id)
    form = QuestionTypeOneForm()
    question = Question_type1.query.filter_by(id=question_id).first()
    form.answer.data = question.correct_answer
    return render_template('editquestion1.html', form = form,title='type1',question = question)

@app.route("/createtype2", methods=['GET', 'POST'])
@login_required
def createtype2():
    form = QuestionType2Form()
    if current_user.is_authenticated and not current_user.is_admin:
        flash('Log in as an admin to create questions.', category='error')
        return redirect(url_for('home'))
    if form.validate_on_submit():
        # DELETE ME BEFORE WE SUBMIT ANYTHING 
        print('Validated!')

        # # If multiple tags were given, split them into a list:
        # tags = form.tags.data.split()
        
        # Construct Question object using the supplied name and param data:
        diff_data = form.difficulty.data
        
        if diff_data == 'Hard':
            mark = 3
        elif diff_data == 'Medium':
            mark = 2
        else: mark = 1

        question = Questiontypetwo(
            title = form.title.data,
            question_text = form.text.data,
            answer = form.answer.data,
            difficulty = form.difficulty.data,
            max_mark = mark,
            author_id = current_user.id,
            feedback = form.feedback.data,
            feedfwd = form.feedfwd.data)

        # Add question to db
        db.session.add(question)
        db.session.commit()

        # Confirm creation for user 
        flash('Question created!', category='success')
        return redirect(url_for('home'))

    return render_template('createtype2.html', title='Create Type 2', form=form, user=current_user)


@app.route("/makeassess", methods=['post','get'])
def makeassess():

    
    questionstype1 = Assessment_questionstype1.query.all()
    questionstype2 = Assessment_questionstype2.query.all()
    print(questionstype1[0].question_type1.question_text)
    print(questionstype2[0].question_type_two.question_text)
    form = TestForm()
    # Logic to add selected question to a new python list in helper.py
    if form.validate_on_submit():
        f = open("aatool\helper.py", "a")
        f.write(form.name.data + "=" +(str(form.chooseQuestions.data)) +"\n" )
        f.close()
        # Print to console to check 
        print(form.chooseQuestions.data)
    return render_template("makeassess.html", data=form.chooseQuestions.data, name=form.name.data, form=form)


@app.route("/takeassess")
def takeassess():
    return render_template('takeassess.html', title='takeassess')

@app.route("/reviewstats")
def reviewstats():
    #Make pie chart
    plt.pie(grade_amounts, labels=grade_labels, autopct='%d%%', colors=colors)
    plt.axis('equal')
    plt.savefig('aatool/static/img/gradepiechart.png')
    #Make CSV file https://www.pythontutorial.net/python-basics/python-write-csv-file/
    with open('aatool/static/Grades.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(grade_labels)
        # write multiple rows
        writer.writerow(string_grades)
    return render_template('reviewstats.html', title='reviewstats', headings=grade_labels, data=string_grades, url='../static/img/gradepiechart.png',
                           recent_assessment=recent_assessment, students_taken=students_taken)



@app.route("/register", methods=['GET','POST'])
def register():
    # Logged in users should not be able to login/register:
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.lower(), 
            email=form.email.data,
            password=form.password.data, 
            firstname=form.firstname.data, 
            surname=form.surname.data)

        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')

        # If registration success, automatically log in the user.
        login_user(user, remember=True)
        return redirect(url_for('home'))

    elif (form.username.data == '' and form.email.data == '' and form.first_name.data == ''):
        flash('Something went wrong with your registration. Check you filled everything in!', category='error')
        return render_template('register.html', title='Register', form=form, user=current_user)
    else: 
        return render_template('register.html', title='Register', form=form, user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Logged in users should not be able to login/register:
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        # Lets users log in using either their email or username.
        user = User.query.filter_by(username = form.username.data.lower()).first()
        email = User.query.filter_by(email = form.username.data.lower()).first()
        
        # Checks for correct username (studentID) first, then email if that fails.
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            print("Logged in as:", user.username)
            flash('You\'ve successfully logged in, '+ current_user.username +'!', category='success')
            return redirect(url_for('home'))
        elif email is not None and email.verify_password(form.password.data):
            login_user(email)
            print("Logged in as:", email.username)
            flash('You\'ve successfully logged in, '+ current_user.username +'!', category='success')
            return redirect(url_for('home'))

        flash('Invalid login credentials, try again.', category='error')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout successful, good bye!', category='success')
    return redirect(url_for('home'))
