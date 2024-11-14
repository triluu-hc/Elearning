from django.db import models
from django.contrib.auth import get_user_model
from .helpers import checkDate,checkDescription,checkOrder,checkText,checkTitle
# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=255, unique=True, validators=[checkTitle])
    description = models.TextField(validators=[checkDescription])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #clean up and trim inputs
    def clean(self):
        checkDate(self.created_at,self.updated_at)
        self.title = self.title.capitalize().strip()
        self.description = self.description.capitalize().strip()
 
class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True, validators=[checkTitle])
    description = models.TextField(validators=[checkDescription])
    order = models.PositiveIntegerField(default=1, unique=True, validators=[checkOrder])
    #clean up and trim inputs
    def clean(self):
        self.title = self.title.strip().capitalize()
        self.description = self.description.strip().capitalize()
class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    class Meta:
        abstract = True

class TextContent(Content):
    text = models.TextField(validators=[checkText])
    #Add validation upon saving to db
    def clean(self):
        self.text = self.text.strip().capitalize()

class VideoContent(Content):
    video_url = models.URLField()