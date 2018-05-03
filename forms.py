from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField, DecimalField, BooleanField

from wtforms import validators, ValidationError

class ContactForm(Form):   
   name = TextField("Name Of Student",[validators.Required("Please enter your name.")])
   Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
   Address = TextAreaField("Address")   
   email = TextField("Email",[validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])   
   Age = IntegerField("age")
   language = SelectField('Languages', choices = [('cpp', 'C++'), ('py', 'Python')])
   submit = SubmitField("Send")

class EmployeeForm(Form):
   employee_name = TextField("Employee Name", [validators.Required("Please enter your full name")])
   username = TextField("User Name", [validators.Required("Please enter your username")])
   user_password = TextField("Password", [validators.Required("Please enter password")])
   email = TextField("Email",[validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])   
   gender = SelectField('Gender', choices = [('M', 'Male'), ('F', 'Female')])
   salary = DecimalField("Salary")
   active = BooleanField("Active")
   submit = SubmitField("Send")
