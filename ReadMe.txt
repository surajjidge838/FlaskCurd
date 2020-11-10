# must learn about Bootstrap classes for components.
Flask CURD application with SQLAlchemy

Part-1:introduction
1) in this application you will learn how to build a flask project.
2) Deal with sqlalachemy ORM tool.
3) working with jinja template
4) template inheritance
5) working with MySql database.
------------------------------------------------------------------------------------
part-2:
Project structure:
1) install Flask, SQLAlchemy
2) create app.py & index.html template
------------------------------------------------------------------------------------
part-3
Design header
1) here we design the header with the help of jinja template
2) create one base.html which is like a common layout template for all html files.
3) inherit the index.html from base.html using jinja template.
4) add all the css & js files in base.html file
5) create header.html file & add this header.html file in index.html file using jinja: {% include 'header.html' %}
------------------------------------------------------------------------------------
part-4
Designing the body
1) create a button to add employee.
2) Also create a table to show employee info in index.html using bootstrap classes.
------------------------------------------------------------------------------------
part-5
Bootstrap Models
1) here we create a models for 'Add new employee' & edit model.
2) so here we toggle bootstrap modal
------------------------------------------------------------------------------------
part-6
Database & Tables
1) create database in MySQl but create table using SQLAlchemy
2) write this sqlalchemy code in app.py
3) import sqlalchemy: from flask_sqlalchemy import SQLAlchemy
4) set the secrete key

in App.py:==>
app.secret_key='secrete_key'

# configure the DB
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@127.0.0.1:3306/flaskcurd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# uri for mysql is:mysql://unm:pwd@localhost/db_name

# create sqlalchemy object
db=SQLAlchemy(app)

5) create modal class in App.py for table:
# modal for table in DB
class Data(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    # create the constructor of this class
    def __init__(self,name,email,phone):
        self.name=name
        self.email=email
        self.phone=phone
# now data modal is ready now we need to add the data model to our CURD DB.

6) fire query using DBoperation.py file like:
from App import db,Data
# to create database use query
db.create_all()

this will create table for you.
------------------------------------------------------------------------------------
part-7
Inserting Data:==>
import request module first from flask
1) to insert data of new user in DB we create the route
@app.route('/insert',methods=['POST'])
def insert():
    if request.method=='POST':
        #get the text input insert into new user modal
        name=request.form['Name']
        email = request.form[ 'Email' ]
        phone = request.form[ 'Phone' ]

        # create object for Data class & pass it to constructor of Data class
        my_data=Data(name,email,phone)
        # insert it into table
        db.session.add(my_data)
        #and commit the session
        db.session.commit()
        # after successfully added into table redirect to index page
        return redirect(url_for('index'))
------------------------------------------------------------------------------------

part-8
Flash message
1) in index.html
     <!-- Display the flash message-->
                {% with messages= get_flashed_messages() %}
                    {% if messages %}
                        {% for message in messages%}
            <!--     display alert message using bootstrap classes-->
                            <div class="alert alert-success alert-dismissable" role="alert">
                                    <button type="button" class="close" data-dismiss="alert" aria-label="close">
                                        <span aria-hidden="true">x</span>
                                    </button>
                                {{ message }}
                            </div>
                        {% endfor %}
                    {% endif %}
                {% endwith %}

                  <!--End flash message-->
------------------------------------------------------------------------------------
part-9
Retrieving data
1) retrieve data in index route
@app.route('/')
def index():
    # retieve data & send to index template
    all_data=Data.query.all()
    return render_template('index.html',employees=all_data)
2) set data in index.html
{% for row in employees %}
                    <!-- this for loop is to display the users info & must be close just
                    before the end table tag else raise an error-->
                    <tr>
                        <td>{{row.id}}</td>
                        <td>{{row.name}}</td>
                        <td>{{row.email}}</td>
                        <td>{{row.phome}}</td>
                        <td>
                            <a href="" class="btn btn-warning btn-xs" data-toggle="modal" data-target="#modaledit">Edit</a>
                            <a href="" class="btn btn-danger btn-xs" data-toggle="modal" onclick="return confirm('Are you sure to Delete ?')">Delete</a>
                        </td>
                    </tr>
{% endfor%} end this loop just before the </table> tag.
------------------------------------------------------------------------------------
part-10
Update users info
1) create a new route for edit form
2)@app.route('/update',methods=['GET','POST'])
def update():
    if request.method == 'POST':
        my_data=Data.query.get(request.form.get('id')) # this is a hidden id from Edit form
        # get the data from update form & set it to the model class & update into db
        my_data.name=request.form['Name']
        my_data.email = request.form[ 'Email' ]
        my_data.phone = request.form['Phone']
        db.session.commit()
        flash('Emp data updated successfully..!')
        # after successful update redirect this to index page
        return redirect(url_for('index'))
3)<form action="{{url_for('update')}}" method="post">
------------------------------------------------------------------------------------
part-11
Delete records
1)<a href="/update/{{row.id}}" class="btn btn-warning btn-xs" data-toggle="modal" data-target="#modaledit{{row.id}}">Edit</a>
  <a href="/delete/{{row.id}}" class="btn btn-danger btn-xs" data-toggle="modal" onclick="return confirm('Are you sure to Delete ?')">Delete</a>

2)@app.route('/delete/<id>',methods=['GET','POST'])
def delete():
    my_data=Data.query.get('id')
    db.session.delete(my_data)
    db.session.commit()
    flash("Data deleted successfully..!")
    return  redirect('index')

