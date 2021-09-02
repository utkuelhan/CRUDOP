from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fy22intern:Abcd1234@fy22interns.northeurope.cloudapp.azure.com/learn'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Intern(db.Model):
    intern_id = db.Column(db.Integer, primary_key=True)
    intern_name = db.Column(db.String(150), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.intern_id

@app.route('/')
def index():
    instructions = "Please select a CRUD operation above"
    return render_template('index.html', instructions=instructions)

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/read')
def read():
    interns = Intern.query.order_by(Intern.date_created)
    return render_template('read.html', interns=interns)


@app.route('/update/<int:intern_id>', methods=['POST', 'GET'])
def update(intern_id):

    interns = Intern.query.order_by(Intern.date_created)

    intern_to_update = db.session.query(Intern).get_or_404(intern_id)

    if request.method == "POST":
        intern_to_update.intern_name = request.form['intern_name']

        if not intern_to_update.intern_name:
            show_error = "You need to fill out the forms required. Please go back and try again."
            return render_template("failu.html", show_error=show_error)

        try:
            db.session.commit()
            return redirect('/read')

        except:
            return "There was a problem updating... Please try again!"

    else:
        return render_template('update.html', intern_to_update=intern_to_update, interns=interns)


@app.route('/update1')
def update1():
    interns = Intern.query.order_by(Intern.date_created)
    return render_template('update1.html', interns=interns)

@app.route('/delete1')
def delete1():
    interns = Intern.query.order_by(Intern.date_created)
    return render_template('delete1.html', interns=interns)

@app.route('/delete/<int:intern_id>')
def delete(intern_id):
    intern_to_delete = db.session.query(Intern).get_or_404(intern_id)
    try:
        db.session.delete(intern_to_delete)
        db.session.commit()
        return redirect('/read')
    except:
        return "There was a problem deleting... Please try again!"

@app.route('/successful', methods=['POST', 'GET'])
def successful():

    if request.method == "POST":
        intern_name = request.form["intern_name"]
        new_intern = Intern(intern_name=intern_name)

        if not intern_name:
            show_error = "You need to fill out the forms required. Please try again."
            return render_template("fail.html", show_error=show_error)

        try:
            db.session.add(new_intern)
            db.session.commit()
            return redirect('/create')

        except:
            return "There was an error adding the new intern! Please try again"

    else:
        interns = Intern.query.order_by(Intern.date_created)
        return render_template("successful.html", interns=interns)



@app.route('/successful0', methods=["POST"])
def successful0():

    intern_id = request.form.get('intern_id')

    if not intern_id:
        show_error = "You need to fill out the forms required. Please try again."
        return render_template("fail0.html", show_error=show_error)

    text = "Thank you, your operation is successfully completed!"
    return render_template('successful0.html', text=text, intern_id=intern_id)