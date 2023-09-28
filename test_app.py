import unittest
import server

from server import app
from model import db, connect_to_db
import crud

from selenium import webdriver
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

    #new User Route Integration Test
    def test_new_user_post_route(self):
        result = self.client.post("/new_user",
                                  data={"fname" : "First",
                                        "lname" : "Last",
                                        "email" : "f.last@gmail.com",
                                        "password" : "test"},
                                  follow_redirects=True)
        
        self.assertIn(b"Favorite Meals", result.data)

    #Confirm User Route Integration Test
    def test_confirm_user_post_route(self):
        result = self.client.post("/confirm_user",
                                data={"email": "test1@gmail.com",
                                    "password": "test"},
                                follow_redirects=True)
        
        self.assertIn(b"Recent Activity", result.data)
    
    # def test_nav_route(self):
    #     result = self.client.post("/get_user_id/json",
    #                             data={"email": "test1@gmail.com",
    #                                 "password": "test"},
    #                             follow_redirects=True)
        
    #     self.assertIn(b"user_id: 1", result.data)
    #     self.assertNotIn(b"user_id: 2", result.data)

    #User profile favorites end to end test
    
    def get_favorites(self):
        email = "test1@gmail.com"
        password = "test"
        driver.get("http://localhost:5000/")
        time.sleep(5)
        driver.find_element_by_id("login-button").click()
        time.sleep(5)
        driver.find_element_by_id("login-email").send_keys(email)
        driver.find_element_by_id("login-password").send_keys(password)
        time.sleep(5)
        driver.find_element_by_id("favorite-meals").click()
        print("Success")

         


   
    

        

if __name__ =="__main__":
    unittest.main()