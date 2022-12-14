from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class EmployeeModel(db.Model):
    __tablename__ = "table"
 
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer(),unique = True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    gender = db.Column(db.String())
    mode = db.Column(db.String())
    position = db.Column(db.String(80))
    email = db.Column(db.String(),unique = True)
 
    def __init__(self, employee_id,name,age,gender,mode,position,email):
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.gender = gender
        self.mode = mode
        self.position = position
        self.email = email
 
    def __repr__(self):
        return f"{self.name}:{self.employee_id}"