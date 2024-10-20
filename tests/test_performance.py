# test_performance.py
import unittest
import json
from app import app, db, Oso
import pytest

class TestOsoAPIPerformance(unittest.TestCase):
    def setUp(self):
        # Configuración inicial de la aplicación en modo de prueba
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usamos una base de datos en memoria para pruebas
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Eliminamos la sesión y las tablas después de cada prueba
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Prueba de rendimiento para crear osos
    @pytest.mark.benchmark
    def test_crear_oso_benchmark(self, benchmark):
        def crear_oso():
            datos = {
                "nombre": "Oso Pardo",
                "especie": "Ursus arctos",
                "edad": 5,
                "peso": 300.5,
                "habitat": "Bosque"
            }
            response = self.app.post('/osos', data=json.dumps(datos), content_type='application/json')
            return response

        # Medimos el rendimiento
        result = benchmark(crear_oso)
        assert result.status_code == 201

    # Prueba de rendimiento para obtener todos los osos
    @pytest.mark.benchmark
    def test_obtener_osos_benchmark(self, benchmark):
        # Primero agregamos varios osos
        for i in range(100):
            nuevo_oso = Oso(nombre=f"Oso {i}", especie="Ursus arctos", edad=5, peso=300.0, habitat="Bosque")
            with app.app_context():
                db.session.add(nuevo_oso)
                db.session.commit()

        # Benchmarking para obtener todos los osos
        def obtener_osos():
            return self.app.get('/osos')

        # Medimos el rendimiento
        result = benchmark(obtener_osos)
        assert result.status_code == 200

    # Prueba de rendimiento para actualizar un oso
    @pytest.mark.benchmark
    def test_actualizar_oso_benchmark(self, benchmark):
        # Primero creamos un oso
        nuevo_oso = Oso(nombre="Oso a Actualizar", especie="Ursus arctos", edad=3, peso=280.0, habitat="Montaña")
        with app.app_context():
            db.session.add(nuevo_oso)
            db.session.commit()

        # Benchmarking para actualizar el oso
        def actualizar_oso():
            datos_actualizados = {
                "nombre": "Oso Actualizado",
                "especie": "Ursus arctos",
                "edad": 4,
                "peso": 310.0,
                "habitat": "Bosque Actualizado"
            }
            return self.app.put(f'/osos/{nuevo_oso.id}', data=json.dumps(datos_actualizados), content_type='application/json')

        # Medimos el rendimiento
        result = benchmark(actualizar_oso)
        assert result.status_code == 200

    # Prueba de rendimiento para eliminar un oso
    @pytest.mark.benchmark
    def test_eliminar_oso_benchmark(self, benchmark):
        # Primero creamos un oso
        nuevo_oso = Oso(nombre="Oso a Eliminar", especie="Ursus arctos", edad=3, peso=290.0, habitat="Tundra")
        with app.app_context():
            db.session.add(nuevo_oso)
            db.session.commit()

        # Benchmarking para eliminar el oso
        def eliminar_oso():
            return self.app.delete(f'/osos/{nuevo_oso.id}')

        # Medimos el rendimiento
        result = benchmark(eliminar_oso)
        assert result.status_code == 200

if __name__ == '__main__':
    unittest.main()
