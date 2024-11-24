from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from courses.models import Course
from attendance.models import Attendance

class AttendanceAPITests(APITestCase):
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
     
        self.attendance = Attendance.objects.create(
            student=self.student,
            course=self.course,
            date="2024-11-20",
            status="present"
        )

        self.teacher_token = self.client.post(
            "/api/users/auth/jwt/create/",
            {"email": "teacher@example.com", "password": "password123"}
        ).data["access"]
        self.student_token = self.client.post(
            "/api/users/auth/jwt/create/",
            {"email": "student@example.com", "password": "password123"}
        ).data["access"]
        self.admin_token = self.client.post(
            "/api/users/auth/jwt/create/",
            {"email": "admin@example.com", "password": "admin123"}
        ).data["access"]

    def test_teacher_can_mark_attendance(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}")
        response = self.client.post("/api/attendance/", {
            "student": self.student.id,
            "course": self.course.id,
            "date": "2024-11-19", 
            "status": "present"
        })
        print(response.data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_can_view_own_attendance(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.student_token}")
        response = self.client.get(f"/api/attendance/{self.attendance.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "present")

    def test_admin_can_view_all_attendance(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get("/api/attendance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)