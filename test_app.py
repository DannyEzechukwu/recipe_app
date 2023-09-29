import unittest
import server

from server import app
from model import db, connect_to_db
import crud

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_driver = "/Users/dannyezechukwu/Desktop/selenium_chrome_driver/chromedriver"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

connect_to_db(app)


class AppTest(unittest.TestCase):

    def setUp(self):
            self.client = app.test_client()
            app.config['TESTING'] = True
    
    #Welcome Page unittest
    def test_welcome_page(self):
        client = server.app.test_client()
        result = client.get("/")
        self.assertIn(b"Welcome Page", result.data)

    #Create Account Page unittest
    def test_create_account_page(self):
        client = server.app.test_client()
        result = client.get("/create_account")
        self.assertIn(b"Becoming a user is easy!", result.data)
    
    #Login Page unittest
    def test_login_page(self):
        client = server.app.test_client()
        result = client.get("/login")
        self.assertIn(b"Get Ready For Your Delicious Experience", result.data)

    # new User Route Integration Test
    def test_new_user_post_route(self):
        result = self.client.post("/new_user",
                                  data={"fname" : "First",
                                        "lname" : "Last",
                                        "email" : "f.last@gmail.com",
                                        "password" : "test"},
                                  follow_redirects=True)
        
        self.assertIn(b"Favorite Meals", result.data)
        crud.delete_user_by_email("f.last@gmail.com")



    #Confirm User Route Integration Test
    def test_confirm_user_post_route(self):
        result = self.client.post("/confirm_user",
                                data={"email": "test1@gmail.com",
                                    "password": "test"},
                                follow_redirects=True)
        
        self.assertIn(b"Recent Activity", result.data)
    

    # User profile favorites End to End test
    def test_get_favorites(self):
        email = "test1@gmail.com"
        password = "test"
        driver.get("http://localhost:5000/")
        time.sleep(3)
        driver.find_element(By.ID,"login-button").click()
        time.sleep(3)
        driver.find_element(By.ID, "login-email").send_keys(email)
        driver.find_element(By.ID, "login-password").send_keys(password)
        driver.find_element(By.ID, "login-submit").click()
        time.sleep(3)
        driver.find_element(By.ID, "removeflash").click()
        time.sleep(3)
        driver.find_element(By.ID, "favorite-meals").click()
        print("Success")

    #Add a meal End to End test
    def test_add_meal(self): 
        email = "test1@gmail.com"
        password = "test"
        fruits = ["apples", "strawberries", "orange", "kiwi"]
        driver.get("http://localhost:5000/")
        time.sleep(3)
        driver.find_element(By.ID,"login-button").click()
        time.sleep(3)
        driver.find_element(By.ID, "login-email").send_keys(email)
        driver.find_element(By.ID, "login-password").send_keys(password)
        driver.find_element(By.ID, "login-submit").click()
        time.sleep(3)
        driver.find_element(By.ID, "removeflash").click()
        time.sleep(3)
        driver.find_element(By.ID, "create_a_meal").click()
        time.sleep(3)
        driver.find_element(By.ID, "meal-name").send_keys("Fruit Salad")
        time.sleep(3)
        driver.find_element(By.ID, "meal-category").send_keys("Fruit")
        time.sleep(3)
        driver.find_element(By.ID, "meal-area").send_keys("Who Knows")
        time.sleep(3)
        driver.find_element(By.ID, "cook-time").click()
        time.sleep(3)
        driver.find_element(By.ID, "20 min").click()
        time.sleep(3)
        driver.find_element(By.ID, "meal-recipe").send_keys("Chill fruit.\nChop fruit.\nServe fruit.")
        time.sleep(3)
        driver.find_element(By.ID, "meal-image").send_keys("https://hips.hearstapps.com/hmg-prod/images/fruit-salad-vertical-jpg-1522181929.jpg?crop=0.696xw:0.464xh;0.252xw,0.286xh&resize=980:*")
        time.sleep(3)
        for i in range(1, 4): 
            driver.find_element(By.ID, f"ingredient{i}").send_keys(f"{fruits[i - 1]}")
            time.sleep(3)
            driver.find_element(By.ID, "ingredient-adder").click()
            time.sleep(3)
            driver.find_element(By.ID, f"measure{i}").send_keys(f"{i}")
        
        driver.find_element(By.ID, "ingredient4").send_keys("kiwi")
        time.sleep(3)
        driver.find_element(By.ID, "measure4").send_keys("4")
        time.sleep(3)
        driver.find_element(By.ID, "url4").send_keys("https://snaped.fns.usda.gov/sites/default/files/styles/crop_ratio_7_5/public/seasonal-produce/2018-05/kiwi.jpg?itok=jv-VEN7M")
        time.sleep(3)
        driver.find_element(By.ID, "adddatmeal").click()
        print("Success")
    
if __name__ =="__main__":
    unittest.main()