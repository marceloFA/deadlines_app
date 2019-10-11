from django.test import TestCase, Client
from django.urls import reverse

from .models import Student


# Create your tests here.
class StudentTestCase(TestCase):

    # Tests for Student objects abnd routes

    def test_login(self):

        # Tests if login works if the Student object exists in the database

        c = Client()
        test_data = {
            "user1": {"username": "TestUser1", "password": "TestPassword1"},
            "user2": {"username": "TestUser2", "password": "TestPassword2"},
        }

        # Student object created for testing
        # Student object user1 is created, User2 is not
        student = Student(**test_data["user1"])
        student.set_password(test_data["user1"]["password"])
        student.save()

        # Login Test

        self.assertTrue(
            c.login(**test_data["user1"])
        )  # c.login() logs on using the credentials provided
        self.assertFalse(
            c.login(**test_data["user2"])
        )  # Since user2 is not created, login attempt fails

    def test_for_response(self):

        # Tests whether the routes return get requests properly

        c = Client()

        # Checking for routes that return webpages
        routes = [
            "/",
            "/events/",
            "/register/",
            "/login/",
            "/password_reset/",
        ]  # List of all the routes that return webpages
        for route in routes:
            response = c.get(route)
            self.assertEqual(response.status_code, 200)

        # Checking for routes that redirect
        routes = ["/logout/"]
        for route in routes:
            response = c.get(route)
            self.assertEqual(response.status_code, 302)


class StudentRegister(TestCase):

    client = Client()
    url = reverse("register")

    def test_register_student_success(self):
        register_data = {
            "name": "a",
            "username": "a",
            "password1": "password",
            "password2": "password",
        }
        response = self.client.post(self.url, register_data)
        # redirects (302) on success
        self.assertEqual(response.status_code, 302)

        student = Student.objects.filter(
            name=register_data.get("name"), username=register_data.get("username")
        )
        self.assertTrue(student.exists())

        student = student.first()

        # match passwords
        self.assertTrue(student.check_password(register_data.get("password1")))

    def test_register_student_mismatched_password(self):
        register_data = {
            "name": "a",
            "username": "a",
            "password1": "password",
            "password2": "something else",
        }
        response = self.client.post(self.url, register_data)
        # returns 200 on failure
        self.assertEqual(response.status_code, 200)

    def test_register_student_missing_username_field(self):
        register_data = {
            "name": "a",
            "password1": "password",
            "password2": "something else",
        }
        response = self.client.post(self.url, register_data)
        # returns 200 on failure
        self.assertEqual(response.status_code, 200)

    def test_register_student_missing_password_field(self):
        register_data = {"name": "a", "username": "a", "password2": "something else"}
        response = self.client.post(self.url, register_data)
        # returns 200 on failure
        self.assertEqual(response.status_code, 200)


class TestStudentActivation(TestCase):

    client = Client()
    deactivate_url = reverse("deactivate")
    reactivate_url = reverse("reactivate")

    def get_student(self):
        student = Student.objects.create(
            username="student", name="student", is_active=True
        )
        student.set_password("password")
        student.save()
        return student

    def test_deactivate_student(self):
        student = self.get_student()
        self.client.force_login(user=student)

        data = {"password": "password"}
        response = self.client.post(self.deactivate_url, data)
        self.assertEqual(response.status_code, 302)
        student.refresh_from_db()
        self.assertFalse(student.is_active)

    def test_deactivate_student_wrong_password(self):
        student = self.get_student()
        self.client.force_login(user=student)

        data = {"password": "something else"}
        response = self.client.post(self.deactivate_url, data)
        self.assertEqual(response.status_code, 200)
        student.refresh_from_db()
        self.assertTrue(student.is_active)

    def test_reactivate_student(self):
        student = self.get_student()
        student.is_active = False
        student.save()

        student.refresh_from_db()

        self.assertFalse(student.is_active)
        self.client.force_login(user=student)

        data = {"username": student.username, "password": "password"}
        response = self.client.post(self.reactivate_url, data)
        self.assertEqual(response.status_code, 302)
        student.refresh_from_db()
        self.assertTrue(student.is_active)

    def test_reactivate_student_wrong_password(self):
        student = self.get_student()
        student.is_active = False
        student.save()

        student.refresh_from_db()

        self.assertFalse(student.is_active)
        self.client.force_login(user=student)

        data = {"username": student.username, "password": "something else"}
        response = self.client.post(self.reactivate_url, data)
        self.assertEqual(response.status_code, 200)
        student.refresh_from_db()
        self.assertFalse(student.is_active)
