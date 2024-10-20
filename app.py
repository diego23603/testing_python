from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# Configuración de la aplicación
app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///osos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Definir el modelo Oso
class Oso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    especie = db.Column(db.String(80), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    habitat = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie,
            "edad": self.edad,
            "peso": self.peso,
            "habitat": self.habitat,
        }


# Crear las tablas
with app.app_context():
    db.create_all()


# Rutas y Métodos CRUD

# Crear un nuevo oso (Create)
@app.route("/osos", methods=["POST"])
def create_oso():
    data = request.get_json()

    required_fields = ["nombre", "especie", "edad", "peso", "habitat"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Datos incompletos"}), 400

    try:
        nuevo_oso = Oso(**{field: data[field] for field in required_fields})
        db.session.add(nuevo_oso)
        db.session.commit()
        return jsonify({"message": "Oso creado exitosamente", "oso": nuevo_oso.to_dict()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error al crear el oso", "details": str(e)}), 500


# Obtener todos los osos (Read)
@app.route("/osos", methods=["GET"])
def get_osos():
    osos = Oso.query.all()
    return jsonify([oso.to_dict() for oso in osos]), 200


# Obtener un oso por ID (Read)
@app.route("/osos/<int:id>", methods=["GET"])
def get_oso(id):
    oso = db.session.get(Oso, id)
    if not oso:
        return jsonify({"error": "Oso no encontrado"}), 404
    return jsonify(oso.to_dict()), 200


# Actualizar un oso por ID (Update)
@app.route("/osos/<int:id>", methods=["PUT"])
def update_oso(id):
    oso = db.session.get(Oso, id)
    if not oso:
        return jsonify({"error": "Oso no encontrado"}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(oso, key):
            setattr(oso, key, value)

    try:
        db.session.commit()
        return jsonify({"message": "Oso actualizado exitosamente", "oso": oso.to_dict()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar el oso", "details": str(e)}), 500


# Eliminar un oso por ID (Delete)
@app.route("/osos/<int:id>", methods=["DELETE"])
def delete_oso(id):
    oso = db.session.get(Oso, id)
    if not oso:
        return jsonify({"error": "Oso no encontrado"}), 404

    try:
        db.session.delete(oso)
        db.session.commit()
        return jsonify({"message": "Oso eliminado exitosamente"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Error al eliminar el oso", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
