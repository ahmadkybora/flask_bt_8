from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

# یک آبجکت از فلسک میسازد
app = Flask(__name__)
# app.secret_key = 'Secret Key'
# app.config['SQLALCHEMEY_DATABASE_URI'] = 'mysql://root:''localhost@flask'
# app.config['SQLALCHEMEY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# یک آبجکت از او آر ام میسازد
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        
@app.route("/")
def index():
    employees = Data.query.all()
    return render_template("index.html", employees=employees)

@app.route("/insert", methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        myData = Data(name, email, phone)
        db.session.add(myData)
        db.session.commit()

        flash("Successfully")

        return redirect(url_for('index'))

@app.route("/update", methods=['POST'])
def update():
    if request.method == 'POST':
        myData = Data.query.get(request.form.get('id'))
        myData.name = request.form['name']
        myData.email = request.form['email']
        myData.phone = request.form['phone']

        db.session.commit()
        flash("updated")

        return redirect(url_for("index"))


@app.route("/delete/<id>", methods=['GET', 'POST'])
def delete(id):
    myData = Data.query.get(id)
    db.session.delete(myData)
    db.session.commit()

    flash("deleted")

    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)