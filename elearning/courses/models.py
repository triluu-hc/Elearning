from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

class Content(models.Model):
    module = models.ForeignKey(Module,related_name='content', on_delete=models.CASCADE)
    class Meta:
        abstract = True

class TextContent(Content):
    text = models.TextField()

class VideoContent(Content):
    video_url = models.URLField()