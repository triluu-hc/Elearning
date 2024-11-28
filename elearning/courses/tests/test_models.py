from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from courses.models import Subject, Course, Module
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