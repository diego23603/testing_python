import unittest
from app import app, db, Oso

class TestOsoModel(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_crear_oso(self):
        with app.app_context():
            oso = Oso(nombre="Yogi", especie="Oso pardo", edad=5, peso=300.5, habitat="Bosque")
            db.session.add(oso)
            db.session.commit()
            self.assertEqual(Oso.query.count(), 1)
            self.assertEqual(Oso.query.first().nombre, "Yogi")

if __name__ == '__main__':
    unittest.main()
