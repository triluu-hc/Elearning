# Import necessary modules for unit testing
import unittest
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from courses.models import Subject, Course, Module, TextContent, VideoContent, Content
from courses.tasks import send_new_course_email, archive_outdated_courses
from django.contrib.auth.models import User



# Unit tests for REST API Endpoints
class SubjectAPITestCase(APITestCase):
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
        data = {'title': 'Advanced Physics', 'code': 'PHY102', 'owner': self.user.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data) 
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.title, 'Advanced Physics')

    def test_delete_subject(self):
        url = reverse('subject-detail', args=[self.subject.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subject.objects.count(), 0)

# Unit tests for Model Methods
class CourseModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.subject = Subject.objects.create(title='Chemistry', code='CHM101', owner=self.user)
        self.course1 = Course.objects.create(subject=self.subject, title='Organic Chemistry', description='Intro to Organic Chemistry')
        self.course2 = Course.objects.create(subject=self.subject, title='Inorganic Chemistry', description='Intro to Inorganic Chemistry')

    def test_course_ordering(self):
        courses = Course.objects.filter(subject=self.subject).order_by('created_at')
        self.assertEqual(courses[0], self.course1)
        self.assertEqual(courses[1], self.course2)
class CourseAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.subject = Subject.objects.create(title='Physics', code='PHY101', owner=self.user)
        self.course = Course.objects.create(subject=self.subject, title='Quantum Mechanics', description='An introduction to quantum mechanics')

    def test_create_course(self):
        url = reverse('subject-courses-list', kwargs={'subject_pk': self.subject.pk})
        data = {'title': 'Classical Mechanics', 'description': 'An introduction to classical mechanics'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        

    def test_retrieve_course(self):
        url = reverse('subject-courses-detail', kwargs={'subject_pk': self.subject.pk, 'pk': self.course.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Quantum Mechanics')

    def test_update_course(self):
        url = reverse('subject-courses-detail', kwargs={'subject_pk': self.subject.pk, 'pk': self.course.pk})
        data = {'title': 'Advanced Quantum Mechanics', 'description': 'Advanced topics in quantum mechanics'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Advanced quantum mechanics')

    def test_delete_course(self):
        url = reverse('subject-courses-detail', kwargs={'subject_pk': self.subject.pk, 'pk': self.course.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.count(), 0)
class ModuleModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.subject = Subject.objects.create(title='Math', code='MTH102', owner=self.user)
        self.course = Course.objects.create(subject=self.subject, title='Algebra', description='Intro to Algebra')
        self.module1 = Module.objects.create(course=self.course, title='Module 1', description='Intro Module', order=2)
        self.module2 = Module.objects.create(course=self.course, title='Module 2', description='Advanced Module', order=1)

    def test_module_ordering(self):
        modules = Module.objects.filter(course=self.course).order_by('order')
        self.assertEqual(modules[0], self.module2)
        self.assertEqual(modules[1], self.module1)

#
class ModuleAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.subject = Subject.objects.create(title='Physics', code='PHY101', owner=self.user)
        self.course = Course.objects.create(subject=self.subject, title='Quantum Mechanics', description='An introduction to quantum mechanics')
        self.module = Module.objects.create(course=self.course, title='Introduction to Quantum', description='Basic concepts', order=1)

    def test_create_module(self):
        url = reverse('course-modules-list', kwargs={'subject_pk': self.subject.pk, 'course_pk': self.course.pk})
        data = {'title': 'Advanced Quantum', 'description': 'Advanced concepts of 30asdasdasdasdasdasdsa', 'order': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.count(), 2)
        
    def test_retrieve_module(self):
        url = reverse('course-modules-detail', kwargs={'subject_pk': self.subject.pk, 'course_pk': self.course.pk, 'pk': self.module.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Introduction to Quantum')

    def test_update_module(self):
        url = reverse('course-modules-detail', kwargs={'subject_pk': self.subject.pk, 'course_pk': self.course.pk, 'pk': self.module.pk})
        data = {'title': 'Quantum Basics', 'description': 'Updated description asdasdasdasdasdasdasdasd'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.module.refresh_from_db()
        self.assertEqual(self.module.title, 'Quantum basics')

    def test_delete_module(self):
        url = reverse('course-modules-detail', kwargs={'subject_pk': self.subject.pk, 'course_pk': self.course.pk, 'pk': self.module.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Module.objects.count(), 0)

class ContentTestsCases(APIClient):
    def setUp(self):
        # Create a test user and authenticate them
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a subject, course, and module for testing
        self.subject = Subject.objects.create(title='Physics', code='PHY101', owner=self.user)
        self.course = Course.objects.create(subject=self.subject, title='Quantum Mechanics', description='Introduction to Quantum Mechanics')
        self.module = Module.objects.create(course=self.course, title='Module 1', description='Basic Quantum Concepts', order=1)

    def test_create_text_content(self):
        url = reverse('module-textcontents-list', kwargs={'subject_pk': self.subject.pk, 'course_pk': self.course.pk, 'module_pk': self.module.pk})
        data = {
            'text': 'Introduction to quantum entanglement, a fundamental aspect of quantum mechanics.'
        }
        response = self.client.post(url, data, format='json')

        # Check if content creation was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TextContent.objects.count(), 1)
        self.assertEqual(TextContent.objects.first().text, data['text'])

    def test_create_video_content(self):
        url = reverse('module-videocontents-list', kwargs={'subject_pk': self.subject.pk, 'course_pk': self.course.pk, 'module_pk': self.module.pk})
        data = {
            'video_url': 'http://example.com/video.mp4'
        }
        response = self.client.post(url, data, format='json')

        # Check if content creation was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VideoContent.objects.count(), 1)
        self.assertEqual(VideoContent.objects.first().video_url, data['video_url'])

    def test_update_text_content(self):
        # Create a TextContent instance
        text_content = TextContent.objects.create(text='Initial content')
        content_type = Content.objects.create(module=self.module, content_type=Content.objects.get_for_model(TextContent), object_id=text_content.id)

        # Update the TextContent
        url = reverse('module-textcontents-detail', kwargs={'subject_pk': self.subject.pk, 'course_pk': self.course.pk, 'module_pk': self.module.pk, 'pk': text_content.pk})
        data = {'text': 'Updated quantum mechanics content'}
        response = self.client.put(url, data, format='json')

        # Check if the update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        text_content.refresh_from_db()
        self.assertEqual(text_content.text, data['text'])

    def test_update_video_content(self):
        # Create a VideoContent instance
        video_content = VideoContent.objects.create(video_url='http://example.com/original.mp4')
        content_type = Content.objects.create(module=self.module, content_type=Content.objects.get_for_model(VideoContent), object_id=video_content.id)

        # Update the VideoContent
        url = reverse('module-videocontents-detail', kwargs={'subject_pk': self.subject.pk, 'course_pk': self.course.pk, 'module_pk': self.module.pk, 'pk': video_content.pk})
        data = {'video_url': 'http://example.com/updated.mp4'}
        response = self.client.put(url, data, format='json')

        # Check if the update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        video_content.refresh_from_db()
        self.assertEqual(video_content.video_url, data['video_url'])

    def test_retrieve_text_content(self):
        text_content = TextContent.objects.create(text='Retrieval test content')
        content = Content.objects.create(module=self.module, content_type=Content.objects.get_for_model(TextContent), object_id=text_content.id)

        url = reverse('module-textcontents-detail', kwargs={'subject_pk': self.subject.pk, 'course_pk': self.course.pk, 'module_pk': self.module.pk, 'pk': text_content.pk})
        response = self.client.get(url, format='json')

        # Check if the retrieval was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], text_content.text)

    def test_retrieve_video_content(self):
        video_content = VideoContent.objects.create(video_url='http://example.com/retrieve.mp4')
        content = Content.objects.create(module=self.module, content_type=Content.objects.get_for_model(VideoContent), object_id=video_content.id)

        url = reverse('module-videocontents-detail', kwargs={'subject_pk': self.subject.pk, 'course_pk': self.course.pk, 'module_pk': self.module.pk, 'pk': video_content.pk})
        response = self.client.get(url, format='json')

        # Check if the retrieval was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['video_url'], video_content.video_url)

    def test_delete_text_content(self):
        text_content = TextContent.objects.create(text='Content to delete')
        content = Content.objects.create(module=self.module, content_type=Content.objects.get_for_model(TextContent), object_id=text_content.id)

        url = reverse('module-textcontents-detail', kwargs={'subject_pk': self.subject.pk, 'course_pk': self.course.pk, 'module_pk': self.module.pk, 'pk': text_content.pk})
        response = self.client.delete(url)

        # Check if the deletion was successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TextContent.objects.count(), 0)

    def test_delete_video_content(self):
        video_content = VideoContent.objects.create(video_url='http://example.com/delete.mp4')
        content = Content.objects.create(module=self.module, content_type=Content.objects.get_for_model(VideoContent), object_id=video_content.id)

        url = reverse('module-videocontents-detail', kwargs={'subject_pk': self.subject.pk, 'course_pk': self.course.pk, 'module_pk': self.module.pk, 'pk': video_content.pk})
        response = self.client.delete(url)

        # Check if the deletion was successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(VideoContent.objects.count(), 0)
# Running the tests
if __name__ == '__main__':
    unittest.main()
