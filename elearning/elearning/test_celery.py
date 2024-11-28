from courses.models import Course
from django.utils import timezone
from datetime import timedelta

old_date = timezone.now() - timedelta(days=100)
course = Course.objects.create(
    title='Old Course',
    description='This course should be archived.',
    subject_id=1,  
)
Course.objects.filter(id=course.id).update(updated_at=old_date)

from courses.tasks import archive_outdated_courses
archive_outdated_courses.delay()

