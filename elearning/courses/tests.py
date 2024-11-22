from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from courses.models import Subject

class SubjectAPITestCase(APITestCase):
    # (Insert the SubjectAPITestCase class code here)
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.subject = Subject.objects.create(title='Physics', code='PHY101', owner=self.user)

    def test_create_subject(self):
        url = reverse('subject-list')
        data = {'title': 'Mathematics', 'code': 'MTH101', 'owner': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subject.objects.count(), 2)
        self.assertEqual(Subject.objects.get(title='Mathematics').code, 'MTH101')

    def test_retrieve_subject(self):
        url = reverse('subject-detail', args=[self.subject.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Physics')
    
    def test_update_subject(self):
        url = reverse('subject-detail', args=[self.subject.pk])
        data = {'title': 'Advanced Physics', 'code': 'PHY102'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.title, 'Advanced Physics')

    def test_delete_subject(self):
        url = reverse('subject-detail', args=[self.subject.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subject.objects.count(), 0)

    