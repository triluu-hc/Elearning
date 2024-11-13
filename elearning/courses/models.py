from django.db import models
from django.contrib.auth import get_user_model
from .helpers import checkDate,checkDescription,checkOrder,checkText,checkTitle
# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Add validation upon saving to db
    def clean(self):
        self.title = checkTitle(self.title)
        self.description = checkDescription(self.description)
        checkDate(self.created_at, self.updated_at)
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    #Add validation upon saving to db
    def clean(self):
        self.title = checkTitle(self.title)
        self.description = checkDescription(self.description)
        checkOrder(self.order)
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    class Meta:
        abstract = True

class TextContent(Content):
    text = models.TextField()
    #Add validation upon saving to db
    def clean(self):
        self.text = checkText(self.text)
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class VideoContent(Content):
    video_url = models.URLField()