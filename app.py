from flask import  Flask, render_template,request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key='secrete_key'

# configure the DB
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@127.0.0.1:3306/flaskcurd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# uri for mysql is:mysql://unm:pwd@localhost/db_name

# create sqlalchemy object
db=SQLAlchemy(app)


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




@app.route('/')
def index():
    # retieve data & send to index template
    all_data=Data.query.all()
    return render_template('index.html',employees=all_data)

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

        flash("Data inserted successfully..!")
        # after successfully added into table redirect to index page
        return redirect(url_for('index'))

@app.route('/update',methods=['GET','POST'])
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

@app.route('/delete/<id>/',methods=['GET','POST'])
def delete(id):
    my_data=Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Data deleted successfully..!")
    return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True) # in production level keep this debug mode to Flase

