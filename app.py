from flask import Flask, request, render_template, redirect, jsonify
from models import db,EmployeeModel
 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()


@app.route('/data/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        mode = request.form['mode']
        position = request.form['position']
        email = request.form['email']
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age, gender=gender, mode=mode, position = position, email=email)

        test = EmployeeModel.query.filter_by(email=email).first()
        if test:
            return jsonify("Email already exist"), 409
        else:
            db.session.add(employee)
            db.session.commit()
            return redirect('/data')


@app.route('/data')
def RetrieveDataList():
    employees = EmployeeModel.query.all()
    # return render_template('datalist.html',employees = employees)
    output = []
    for employee in employees:
        my_dict= {"employee_id": employee.employee_id,"employee_name":employee.name}
        output.append(my_dict)
    return jsonify(output)


@app.route('/data/<int:id>')
def RetrieveSingleEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        # return render_template('data.html', employee = employee)
        return jsonify(
        employee_id = employee.employee_id,
        name = employee.name,
        age = employee.age,
        gender = employee.gender,
        mode = employee.mode,
        position = employee.position,
        email = employee.email
        )   
    return f"Employee with id ={id} Doenst exist"


@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
 
            name = request.form['name']
            age = request.form['age']
            gender = request.form['gender']
            mode = request.form['mode']
            position = request.form['position']
            email = request.form['email']
            employee = EmployeeModel(employee_id=id, name=name, age=age, gender=gender, mode=mode, position = position, email=email)
 
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does nit exist"
 
    return render_template('update.html', employee = employee)


@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect('/data')
        abort(404)
 
    return render_template('delete.html')
    

app.run(host='localhost', port=5050)
