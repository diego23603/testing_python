import unittest
import json
from app import app, db

class TestAPIIntegration(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_crear_y_obtener_oso(self):
        # Crear un oso
        response = self.app.post('/osos', 
                                 data=json.dumps({
                                     "nombre": "Yogi",
                                     "especie": "Oso pardo",
                                     "edad": 5,
                                     "peso": 300.5,
                                     "habitat": "Bosque"
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        # Obtener el oso creado
        response = self.app.get('/osos/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['nombre'], "Yogi")

if __name__ == '__main__':
    unittest.main()
