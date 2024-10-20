import unittest
import json
from app import app, db, Oso

class TestOsoAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_crear_oso(self):
        response = self.app.post('/osos',
                                 data=json.dumps({'nombre': 'Yogi', 'especie': 'Oso pardo', 'edad': 5, 'peso': 300}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['nombre'], 'Yogi')

    def test_obtener_osos(self):
        self.app.post('/osos',
                      data=json.dumps({'nombre': 'Yogi', 'especie': 'Oso pardo', 'edad': 5, 'peso': 300}),
                      content_type='application/json')
        response = self.app.get('/osos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nombre'], 'Yogi')

    def test_obtener_oso(self):
        response = self.app.post('/osos',
                                 data=json.dumps({'nombre': 'Yogi', 'especie': 'Oso pardo', 'edad': 5, 'peso': 300}),
                                 content_type='application/json')
        oso_id = json.loads(response.data)['id']
        response = self.app.get(f'/osos/{oso_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['nombre'], 'Yogi')

    def test_actualizar_oso(self):
        response = self.app.post('/osos',
                                 data=json.dumps({'nombre': 'Yogi', 'especie': 'Oso pardo', 'edad': 5, 'peso': 300}),
                                 content_type='application/json')
        oso_id = json.loads(response.data)['id']
        response = self.app.put(f'/osos/{oso_id}',
                                data=json.dumps({'nombre': 'Boo Boo', 'edad': 6}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['nombre'], 'Boo Boo')
        self.assertEqual(data['edad'], 6)

    def test_eliminar_oso(self):
        response = self.app
