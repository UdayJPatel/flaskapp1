from flask import Flask, render_template, redirect, url_for, request, flash
from forms import ContactForm, EmployeeForm
import pymysql

app = Flask(__name__)
app.secret_key = 'development key'





@app.route('/contact', methods = ['GET', 'POST'])
def contact():
   form = ContactForm()
   pageTitle = "Contact Form"
   
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('contact.html', form = form, pageTitle = pageTitle)
      else:
         return render_template('success.html')
   elif request.method == 'GET':
      return render_template('contact.html', form = form, pageTitle = pageTitle)





@app.route('/employee', methods = ['GET', 'POST'])
def employee():
   form = EmployeeForm()
   pageTitle = "Employee Form"
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('employee.html', form = form, pageTitle = pageTitle)
      else:
         print('Doing employeeadd')
         result = employeeAdd(request.form)
         if result['error'] == 1:
            return render_template('employee.html', form = form, pageTitle = pageTitle, processMessage = result['message'])
         else:
            return redirect(url_for('employeelist'))

         return render_template('employeeadd.html', formData = request.form)
   elif request.method == 'GET':
      return render_template('employee.html', form = form, pageTitle = pageTitle)


def employeeAdd(formData):
   # print(formData)   
   if 'active' not in formData:
      active = 0
   else:
      active = 1
   db = pymysql.connect("localhost","localCentosUser","Pa55word","employees" )
   cursor = db.cursor()
   sql = "SELECT 1 from employee where employee_name = '%s' or username = '%s' or email = '%s';" %(formData['employee_name'],formData['username'],formData['email'])
   cursor.execute(sql)
   retDict = {}
   retDict['message'] = '<div class = "text-danger bg-info">Employee %s added successfully</div>' %(formData['employee_name'])
   retDict['error'] = 0
   if cursor.rowcount > 0:
      retDict['error'] = 1
      retDict['message'] = 'Employee %s already exists' %formData['employee_name']
   else:
      sql = "insert into employee (employee_name,username,user_password,email,gender,salary,active)\
      values('%s','%s','%s','%s','%s',%d,%d)" \
      %(formData['employee_name'],\
         formData['username'],\
         formData['user_password'],\
         formData['email'],\
         formData['gender'],\
         int(formData['salary']),\
         active)
      

   print('And the sql is: %s' %sql)
   cursor.execute(sql)
   db.commit()
   # disconnect from server
   db.close()
   return retDict




@app.route('/employeelist', methods = ['GET', 'POST'])
def employeelist():
   form = EmployeeForm()
   pageTitle = "Employee List"
   
   if request.method == 'GET':
      # Open database connection
      db = pymysql.connect("localhost","localCentosUser","Pa55word","employees" )

      # prepare a cursor object using cursor() method
      cursor = db.cursor()

      # execute SQL query using execute() method.
      cursor.execute("SELECT VERSION()")

      # Fetch a single row using fetchone() method.
      data = cursor.fetchone()
      print ("Database version : %s " % data)

      #now lets fetch records
      cursor.execute("INSERT INTO employee (employee_name,username,user_password,email,gender,salary,active) SELECT * FROM (SELECT 'Darshan Patel','dpxx56','123123','dpxxr@att.com','M',565656,0) AS tmp WHERE NOT EXISTS (SELECT 1 FROM employee WHERE employee_name = 'Darshan Patel') LIMIT 1;")
      db.commit()
      cursor.execute("SELECT * FROM employee;")
      data = cursor.fetchall()      
      print('Total records: %d' %cursor.rowcount)

      # disconnect from server
      db.close()

      columnList = ('id','employee_name','username','user_password','email','gender','salary','active')

      return render_template('employeelist.html', pageTitle = pageTitle, data = data, columnList = columnList)





@app.route('/helloworld')
def hello_world():
   return 'Hello World'

def hello_canada():
   return 'Hello Canada'
app.add_url_rule('/canada', 'canada', hello_canada)

@app.route('/user/<name>')
def hello_user(name):
   return 'Hello %s' %name


@app.route('/')
def index():
   return render_template('index.html')

@app.route('/sampleform',methods=['POST','GET'])
def sampleform():
   requestData = {}
   formData = {}
   formData['firstName'] = 'First Name'
   formData['lastName'] = 'Last name'

   if request.args:
      formData = request.args
   if request.form:
      formData = request.form

   try:
      requestData['method'] = request.method
      requestData['form'] = request.form
      requestData['args'] = request.args
      requestData['cookies'] = request.cookies
   except NameError:
      requestData['error'] = "Request scope not available yet"   
   
   return render_template('sampleform.html',requestData = requestData, formData = formData)

@app.route('/hello')
def hello(name='Flask'):
   print('name: %s' %name)
   return render_template('index.html', name = name)


@app.route('/hello/<name>')
def hellouser(name):
   return redirect(url_for('hello', name = name))

@app.route('/hellomember/<name>')
def hellomember(name):
   return render_template('index.html', name = name)

@app.route('/hellosamplejson')
def hellosamplejson():
   fruits=['Apple','Mango','Grapes']
   person = {'firstname':'Uday','lastname':'Patel','Address':{'street':'Rohan Jharoka','City':'Bangalore','State':'karnataka'},'Cell':8971495919}
   return render_template('index.html', fruits = fruits, person = person)

if __name__ == '__main__':
   app.run(debug = True, host = '0.0.0.0')
