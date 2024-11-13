from django.contrib import admin
from .models import Course, Module, TextContent, VideoContent

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','created_at', 'updated_at')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')

@admin.register(TextContent)
class TextContentAdmin(admin.ModelAdmin):
    list_display = ('module', 'text')

@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ('module', 'video_url')
