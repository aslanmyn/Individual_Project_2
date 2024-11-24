from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from .models import Student

class StudentAPITests(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            email="admin@example.com", password="admin123", role="admin"
        )
        self.student_user = CustomUser.objects.create_user(
            email="student@example.com", password="student123", role="student"
        )
        self.student_profile = Student.objects.create(
            user=self.student_user, full_name="Student User"
        )
        self.admin_token = self.client.post(
            "/api/users/auth/jwt/create/",
            {"email": "admin@example.com", "password": "admin123"},
        ).data["access"]
        self.student_token = self.client.post(
            "/api/users/auth/jwt/create/",
            {"email": "student@example.com", "password": "student123"},
        ).data["access"]

    def test_admin_can_view_all_students(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get("/api/students/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_can_view_own_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.student_token}")
        response = self.client.get("/api/students/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["full_name"], "Student User")

    def test_student_cannot_view_other_profiles(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.student_token}")
        other_student = CustomUser.objects.create_user(
            email="otherstudent@example.com", password="other123", role="student"
        )
        Student.objects.create(user=other_student, full_name="Other Student")
        response = self.client.get("/api/students/")
        self.assertEqual(len(response.data), 1)