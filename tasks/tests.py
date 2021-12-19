from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task


class TaskTest(APITestCase):
    def setUp(self):
        Task.objects.create(title="test title", author_ip='127.0.0.1')
        Task.objects.create(title="test title2", author_ip='127.0.0.1')
        return super().setUp()

    def test_delete_task(self):
        response = self.client.delete('/todolist/1', follow=True)
        response2 = self.client.delete('/todolist/3', follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_task(self):
        response = self.client.get('/todolist/2', follow=True)
        response2 = self.client.get('/todolist/3', follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_tasks(self):
        response = self.client.get('/todolist/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_task(self):
        data = {"title": "test title"}
        data2 = {"title": "test title2", "done": True,
                 "done_date": timezone.now()}
        data3 = {"title": "test title3", "done": True}
        data4 = {"title": "test title4", "done": False,
                 "done_date": timezone.now()}
        data5 = {"done": True}

        response = self.client.post('/todolist/', data, format='json')
        response2 = self.client.post('/todolist/', data2, format='json')
        response3 = self.client.post('/todolist/', data3, format='json')
        response4 = self.client.post('/todolist/', data4, format='json')
        response5 = self.client.post('/todolist/', data5, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['done'], False)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)
