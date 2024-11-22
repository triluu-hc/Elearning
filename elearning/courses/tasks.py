from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import Course
from django.utils import timezone
from datetime import timedelta
import logging
@shared_task
def send_new_course_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subject_pk = course.subject.pk
        subject_title = course.subject.title
        course_id = course.id
        course_title = course.title
        course_description = course.description
        # Construct the URL as per your requirement
        course_url = f"{settings.SITE_URL}/api/subjects/{subject_pk}/courses/{course_id}/"

        email_subject = f"New Course Created in {subject_title}: {course_title}"
        message = (
            f"A new course titled '{course_title}' has been created in the subject '{subject_title}'.\n\n"
            f"Description:\n{course_description}\n\n"
            f"View the course here: {course_url}"
        )
        recipient_list = ['testuser1@example.com', 'testuser2@example.com']  # Replace with actual recipients

        send_mail(
            email_subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
    except Course.DoesNotExist:
        # Handle the case where the course does not exist
        pass

logger = logging.getLogger(__name__)

@shared_task
def archive_outdated_courses():
    threshold_date = timezone.now() - timedelta(days=365)  # Adjust the number of days as needed
    outdated_courses = Course.objects.filter(updated_at__lt=threshold_date, is_archived=False)
    count = outdated_courses.update(is_archived=True)
    logger.info(f"Archived {count} outdated courses.")
    return f"Archived {count} outdated courses."