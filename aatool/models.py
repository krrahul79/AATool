from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from aatool import login_manager, db
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
import matplotlib.pyplot as plt
from datetime import datetime



class Assessment_questionstype1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column( db.Integer, db.ForeignKey('assessment.id'),nullable=False)
    question_type1_id = db.Column(db.Integer, db.ForeignKey('question_type1.id'),nullable=False)

class Assessment_questionstype2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column( db.Integer, db.ForeignKey('assessment.id'),nullable=False)
    question_type2_id = db.Column(db.Integer, db.ForeignKey('question_type_two.id'),nullable=False)



class Question_type1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    option_one = db.Column(db.Text, nullable=False)
    option_two = db.Column(db.Text, nullable=False)
    option_three = db.Column(db.Text, nullable=False)
    option_four = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)
    assessment_questionstype1 = db.relationship('Assessment_questionstype1', backref='question_type1', lazy=True)
    
   
   

def __repr__(self):
    return f"Question_type1('{self.question_text}', '{self.option_one}', '{self.option_two}', '{self.option_three}', '{self.option_four}')"



# Draft of asssessment model (including question relationships)
class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    overall_test_feedback_fail = db.Column(db.Text, nullable=True)
    overall_test_feedback_pass = db.Column(db.Text, nullable=True)
    overall_test_feedback_merit = db.Column(db.Text, nullable=True)
    overall_test_feedback_dist= db.Column(db.Text, nullable=True)
    is_summative=db.Column(db.Boolean,nullable=False,default=False)
    assessment_questionstype1 = db.relationship('Assessment_questionstype1', backref='assessment', lazy=True)
    assessment_questionstype2 = db.relationship('Assessment_questionstype2', backref='assessment', lazy=True)
    # question_type1 = db.relationship('Question_type1', secondary = assessment_questionstype1)
    # questions2 = db.relationship('Questiontypetwo', secondary = assessment_questionstype2)






def __repr__(self):
    return f"Assessment('{self.date}', '{self.category}', '{self.overall_test_feedback_fail}', '{self.overall_test_feedback_pass}','{self.overall_test_feedback_merit}', '{self.overall_test_feedback_dist}')"




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    firstname = db.Column(db.String(15), nullable=False)
    surname = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text())
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False,default=False, unique=False)
    assessment = db.relationship('Assessment', backref='user', lazy=True)
    
    # Can't use modules table yet until we figure out the m:n relationship
    # modules = db.Relationship('Module', backref='Question', passive_deletes=True, lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        return f"User(ID: {self.student_ID}, Email: {self.email}, Admin status: {self.is_admin})"
    

class Questiontypetwo(db.Model):
    __tablename__ = "question_type_two"
    id = db.Column(db.Integer, primary_key=True)
    title = (db.Column(db.String(64), nullable=False, unique=True))
    date_created = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    question_text = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Integer(), nullable=False, unique=False)
    difficulty = db.Column(db.String(8), nullable=False, unique=False)
    max_mark = db.Column(db.Integer, default=1, unique=False, nullable=False) 
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    feedback = db.Column(db.Text, nullable=True, unique=False)
    feedfwd = db.Column(db.Text, nullable=True, unique=False)
    assessment_questionstype2 = db.relationship('Assessment_questionstype2', backref='question_type_two', lazy=True)

    #moduleList = db.relationship('Module', backref='Question', passive_deletes=True, lazy=True)
         #Commented out bc we dont have Module model/table (yet).

    def __repr__(self):
        return f"QuestionTypeTwo('{self.question_text}', '{self.answer}', '{self.date_created}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Tilly's code - to be tidied
test_results = {"s001": 91, "s002": 65, "s003": 54, "s004": 82, "s005": 77, "s006":73, "s007":76, "s008":85, "s009": 74, "s010": 80,
               "s011": 72, "s012": 50, "s013": 41, "s014": 0, "s015": 93, "s016": 88, "s017": 91, "s018": 70, "s019": 69, "s020": 80}

assessments = ["CMT313 Assessment 3"]
recent_assessment = assessments[len(assessments)-1]

students_taken = len(test_results.keys())

grade_labels = ["Distinction", "Merit", "Pass", "Fail"]

colors = ['#028397','#0299b1','#03dbfc','#68e9fd']

test_marks = test_results.values()
dist = 0
merit = 0
passmark = 0
fail = 0
for i in test_marks:
    if i >= 70:
        dist +=1
    elif i >= 60:
        merit += 1
    elif i>= 50:
        passmark += 1
    else:
        fail += 1
        
grade_amounts=[dist,merit,passmark,fail]
string_grades = []
for i in grade_amounts:
    string_grades.append(str(i))