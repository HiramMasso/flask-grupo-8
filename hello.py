from sqlalchemy import text
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Tipos de metodos:
# GET -> Se utiliza para recuperar informacion del servidor
# POST -> Se utiliza para enviar datos al servidor para su procesamiento
# DELETE -> Se utiliza para eliminar uno o mas recursos en el servidor o BD
# PUT -> Se utiliza para actualizar un recurso en el servidor
# PATCH -> Se utiliza para actualizar parcialmente un recurso en el servidor

app = Flask(__name__)
CORS(app)

# configuracion de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:11052000@localhost:5432/students2'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = 'FALSE'

db = SQLAlchemy(app)

#definicion del modelo de estudiante (modelo = tabla de base de datos es lo mismo)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'major': self.major
        }
    
#crear las tablas
with app.app_context():
    db.create_all()
    
    #verificar la conexion a la base de datos
    try:
        #realizar una consulta simple
        db.session.execute(text('SELECT 1'))
        print('conexion a la base de datos exitosa')
    except Exception as e:
        print(f'error al conectar: {e}')
        

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

# @app.route('/oplesk', methods=['GET','POST','DELETE','PUT','PATCH'])
# def social_oplesk():
#     return '<h1> Hello; from oplesk </h1>'


#  Ruta para obtener estudiantes
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

#  Ruta para obtener un estudiante por params ( Por parametro de ruta )
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    student = Student.query.get(student_id)
    if student:
        return jsonify(student.to_dict())
    return jsonify({'message': 'student not found'})
    

# Ruta para crear un estudiante.
@app.route('/create-student', methods=['POST'])
def create_student():
    data = request.json
    new_student = Student(name = data['name'], age = data['age'], major = data['major'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message:': 'student creation succesfully',
                    'data': new_student.to_dict()})

# Ruta para borrar todos los estudiantes
@app.route('/delete-students', methods=['DELETE'])
def delete_all_students():
    db.session.query(Student).delete()
    db.session.commit()
    return jsonify({'message': 'Estudiantes borrados correctamente'})

# Ruta para actualizar parcialmente un estudiante
@app.route('/patch-student/<int:student_id>', methods=['PATCH'])
def update_one_student(student_id):
    data = request.json
    student = Student.query.get(student_id)
    if student:
        for key, value in data.items():
            setattr(student, key, value)
        db.session.commit()
        return jsonify({'message': 'Estudiante actualizado parcialmente', 'data': student.to_dict()})
    return jsonify({'message': 'student not found'})

# Ruta para eliminar un estudiante por query params
@app.route('/delete-student/', methods=['DELETE'])
def delete_student_by_name():
    name = request.args.get('name')
    student = Student.query.filter_by(name=name).first()
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': f'student {name} deleted succesfully'})
    return jsonify({'message': 'student not found'})