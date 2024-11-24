from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from notifications.models import Notification, NotificationTemplate


class NotificationAPITests(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            email="admin@example.com", password="admin123", role="admin", username="admin_user"
        )
        self.student = CustomUser.objects.create_user(
            email="student@example.com", password="student123", role="student", username="student_user"
        )

        self.template = NotificationTemplate.objects.create(
            title="Grade Update",
            message="Your grade for {course_name} has been updated to {grade}."
        )

        self.notification = Notification.objects.create(
            recipient=self.student,
            template=self.template,
            message=self.template.message.format(course_name="Math", grade="A"),
            recipient_role="student",
            status="pending"
        )

        self.admin_token = self.client.post(
            "/api/users/auth/jwt/create/",
            {"email": "admin@example.com", "password": "admin123"}
        ).data["access"]

        self.student_token = self.client.post(
            "/api/users/auth/jwt/create/",
            {"email": "student@example.com", "password": "student123"}
        ).data["access"]

    def test_admin_can_create_notification(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.post("/api/notifications/", {
            "recipient": self.student.id,
            "template": self.template.id,
            "message": "Custom message for student",
            "recipient_role": "student",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["recipient"], self.student.id)

    def test_student_can_view_notifications(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.student_token}")
        response = self.client.get("/api/notifications/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["message"], self.notification.message)