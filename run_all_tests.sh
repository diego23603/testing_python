#!/bin/bash

echo "Ejecutando pruebas unitarias y de integración..."
python -m unittest discover tests

echo "Ejecutando pruebas de rendimiento..."
pytest tests/test_performance.py

echo "Ejecutando pruebas de seguridad..."
python -m unittest tests/test_security.py

echo "Ejecutando pruebas funcionales..."
python -m unittest tests/test_functional.py

echo "Para ejecutar pruebas de carga, use: locust -f locustfile.py"
