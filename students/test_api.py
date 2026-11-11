from rest_framework.test import APITestCase
from students.models import Student

from django.contrib.auth.models import User
from rest_framework import status

class StudentAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="User@123"
        )
        self.other_user = User.objects.create_user(
            username="user2",
            password="User@1234"
        )

        self.student = Student.objects.create(
            user = self.user,
            name="Rahul",
            age=22,
            email="rahul@example.com",
            phone="2334455667",
            marks=87,
            city="Mohali"
        )
        self.list_url = "/api/students/"

    def test_unauthenticated_user_cannot_list_students(self):
        response = self.client.get(self.list_url)

        self.assertEquals(
            response.status_code, # 401
            status.HTTP_401_UNAUTHORIZED
        )

    def test_authenticated_user_can_list_students(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.list_url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 1)

    def test_user_cannot_access_another_users_student(self):
        self.client.force_login(user=self.other_user)

        response = self.client.get(
            f"{self.list_url}{self.student.id}/"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_authenticated_user_can_create_student(self):
        self.client.force_login(user=self.user)

        data = {
            "name": "Aman",
            "age": 21,
            "email": "aman@example.com",
            "phone": "9123456780",
            "marks": 78,
            "city": "Chandigarh",
            "course": None,
            "skills": [],
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Student.objects.filter(
                user=self.user,
                email="aman@example.com"
            ).exists()
        )
        