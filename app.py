
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.secret_key="hello"
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
   
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    phone=db.Column(db.Integer)
    def __init__(self,name,Email,Phone):
        self.name=name
        self.email=Email
        self.phone=Phone

@app.route('/')
def Index():
    all_data=Data.query.all()
    return  render_template("index.html",students=all_data)
@app.route('/insert',methods=['POST'])
def insert():
    
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        phone=request.form["phone"]
        my_data=Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
        flash("Student inserted Successfully")
        return redirect(url_for('Index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    student = Data.query.get(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.email = request.form['email']
        student.phone = request.form['phone']
        db.session.commit()
        flash("Student Updated Successfully")
        return redirect(url_for('Index'))
    return render_template('index.html', student=student, students=Data.query.all())

    

@app.route('/delete/<id>/',methods=['GET','POST'])
def delete(id):
    my_data=Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("data deleted successfully")
    return redirect(url_for('Index'))
    




if __name__ == '__main__':
    app.run(debug=True)