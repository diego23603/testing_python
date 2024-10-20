import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestFunctional(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  # Asegúrate de tener ChromeDriver instalado
        self.driver.get("http://localhost:5000")

    def tearDown(self):
        self.driver.quit()

    def test_crear_oso(self):
        # Aquí deberías implementar los pasos para crear un oso a través de la interfaz
        # Este es solo un ejemplo y necesitarás adaptar según tu interfaz real
        self.driver.find_element(By.ID, "nombre").send_keys("Yogi")
        self.driver.find_element(By.ID, "especie").send_keys("Oso pardo")
        self.driver.find_element(By.ID, "edad").send_keys("5")
        self.driver.find_element(By.ID, "peso").send_keys("300.5")
        self.driver.find_element(By.ID, "habitat").send_keys("Bosque")
        self.driver.find_element(By.ID, "submit").click()

        # Esperar a que aparezca el mensaje de éxito
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "success-message"))
        )

        self.assertTrue("Oso creado exitosamente" in self.driver.page_source)

if __name__ == "__main__":
    unittest.main()
