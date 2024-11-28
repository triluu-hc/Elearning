from unittest.mock import patch
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from courses.models import Subject, Course
from courses.tasks import send_new_course_email, archive_outdated_courses

class CeleryTasksTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.subject = Subject.objects.create(title='Biology', code='BIO101', owner=self.user)
        self.course = Course.objects.create(subject=self.subject, title='Genetics', description='Intro to Genetics')
        # Setting the course to be outdated
        self.course.updated_at = timezone.now() - timedelta(days=365)
        self.course.save()

    @patch('courses.tasks.send_mail')
    def test_send_new_course_email(self, mock_send_mail):
        send_new_course_email(self.course.id)
        mock_send_mail.assert_called_once()
        args, kwargs = mock_send_mail.call_args
        self.assertIn('New Course Created', args[0])  # Check subject of the email
        self.assertIn(self.course.title, args[0])
        self.assertIn(self.course.description, args[1])  # Check message body
        self.assertEqual(kwargs['recipient_list'], ['user@example.com'])

    def test_archive_outdated_courses(self):
        archive_outdated_courses()
        self.course.refresh_from_db()
        self.assertTrue(self.course.is_archived)