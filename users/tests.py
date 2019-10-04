from django.test import TestCase, Client
from .models import Student
from apps import urls

# Create your tests here.
class StudentTestCase(TestCase):

    # Tests for Student objects abnd routes

    def test_login(self):
       
       # Tests if login works if the Student object exists in the database

       c = Client()
       test_data = {
           'user1':{
               'username': 'TestUser1',
               'password': 'TestPassword1'
           },
           'user2':{
               'username': 'TestUser2',
               'password': 'TestPassword2'
           }
       }

       # Student object created for testing
       # Student object user1 is created, User2 is not
       student = Student(**test_data['user1'])
       student.set_password(test_data['user1']['password'])
       student.save()

       # Login Test

       self.assertTrue(c.login(**test_data['user1']))  # c.login() logs on using the credentials provided
       self.assertFalse(c.login(**test_data['user2'])) # Since user2 is not created, login attempt fails

     
    def test_for_response(self):

        # Tests whether the routes return get requests properly 

        c = Client()

        # Checking for routes that return webpages
        routes = ['/','/tasks/','/register/','/login/','/password_reset/'] # List of all the routes that return webpages
        for route in routes:
            response = c.get(route)
            self.assertEqual(response.status_code,200)

        # Checking for routes that redirect
        routes = ['/logout/']
        for route in routes:
            response = c.get(route)
            self.assertEqual(response.status_code,302)