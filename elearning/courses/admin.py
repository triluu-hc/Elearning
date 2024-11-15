from django.contrib import admin
from .models import Course, Module, TextContent, VideoContent, Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'owner')
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','created_at', 'updated_at')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')

@admin.register(TextContent)
class TextContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')

@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_url')
