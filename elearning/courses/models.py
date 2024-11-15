from django.db import models
from .helpers import checkDate,checkDescription,checkOrder,checkText,checkTitle
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class Subject(models.Model):
    title = models.CharField(max_length=255, unique=True, validators=[checkTitle])
    code = models.CharField(max_length=6, unique=True)
    owner = models.ForeignKey(User,related_name='subjects', on_delete=models.CASCADE)


class Course(models.Model):
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, validators=[checkTitle])
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
    title = models.CharField(max_length=255, validators=[checkTitle])
    description = models.TextField(validators=[checkDescription])
    order = models.PositiveIntegerField(default=1, validators=[checkOrder])
        
    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order')
    #clean up and trim inputs
    def clean(self):
        self.title = self.title.strip().capitalize()
        self.description = self.description.strip().capitalize()
class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1, validators=[checkOrder])
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ('textcontent', 'videocontent')}
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['order']
        unique_together = ('module', 'order')

class TextContent(models.Model):
    text = models.TextField(validators=[checkText])
    #Add validation upon saving to db
    def clean(self):
        self.text = self.text.strip().capitalize()

class VideoContent(models.Model):
    video_url = models.URLField()