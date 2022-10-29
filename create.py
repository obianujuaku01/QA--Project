from flask import Flask, render_template, request, redirect
from models import db, StudentModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        student = StudentModel(student_id=student_id, name=name, age=age, position=position)
        db.session.add(student)
        db.session.commit()
        return redirect('/data')


@app.route('/data')
def RetrieveList():
    students = StudentModel.query.all()
    return render_template('datalist.html', students=students)


@app.route('/data/<int:id>')
def RetrieveStudent(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    if student:
        return render_template('data.html', student=student)
    return f"Student with id ={id} Doesnt exist"


@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            student = StudentModel(student_id=id, name=name, age=age, position=position)
            db.session.add(student)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Student with id = {id} Does nit exist"

    return render_template('update.html', student=student)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')


app.run(host='localhost', port=5000)
