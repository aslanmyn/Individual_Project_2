from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from courses.models import Course
from grades.models import Grade


class GradeAPITests(APITestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.create_user(
            email="teacher@example.com",
            password="password123",
            role="teacher",
            username="teacher_user"
        )
        self.student = CustomUser.objects.create_user(
            email="student@example.com",
            password="password123",
            role="student",
            username="student_user"
        )
        self.admin = CustomUser.objects.create_user(
            email="admin@example.com",
            password="admin123",
            role="admin",
            username="admin_user"
        )
        self.course = Course.objects.create(
            name="Physics",
            description="Physics Course",
            instructor=self.teacher
        )
        self.grade = Grade.objects.create(
            student=self.student,
            course=self.course,
            grade=85.0,
            teacher=self.teacher
        )
        self.teacher_token = self.client.post(
            "/api/users/auth/jwt/create/",
            {"email": "teacher@example.com", "password": "password123"},
        ).data["access"]
        self.student_token = self.client.post(
            "/api/users/auth/jwt/create/",
            {"email": "student@example.com", "password": "password123"},
        ).data["access"]
        self.admin_token = self.client.post(
            "/api/users/auth/jwt/create/",
            {"email": "admin@example.com", "password": "admin123"},
        ).data["access"]

    def test_teacher_can_assign_grade(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}")

        Grade.objects.filter(student=self.student, course=self.course).delete()

        response = self.client.post("/api/grades/", {
            "student": self.student.id,
            "course": self.course.id,
            "grade": 90.0
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["grade"], "90.00") 

    def test_student_can_view_own_grade(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.student_token}")
        response = self.client.get(f"/api/grades/{self.grade.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data["grade"]), 85.0)  

    def test_admin_can_view_all_grades(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get("/api/grades/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_teacher_cannot_assign_negative_grade(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}")
        response = self.client.post("/api/grades/", {
            "student": self.student.id,
            "course": self.course.id,
            "grade": -10.0
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("grade", response.data)

    def test_student_cannot_create_grade(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.student_token}")
        response = self.client.post("/api/grades/", {
            "student": self.student.id,
            "course": self.course.id,
            "grade": 95.0
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_grade(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.delete(f"/api/grades/{self.grade.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Grade.objects.filter(id=self.grade.id).exists())

    def test_teacher_cannot_delete_grade(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}")
        response = self.client.delete(f"/api/grades/{self.grade.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)