from rest_framework import serializers
from .models import Course, Module, TextContent, VideoContent
from .helpers import checkDate,checkDescription,checkOrder,checkText,checkTitle
class TextContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextContent
        fields = '__all__'

class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = '__all__'
    
class ModuleSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'contents']
    #validate inputs at serializers
    def validate_title(self, value):
        return checkTitle(value)
    def validate_description(self, value):
        return checkDescription(value)
    def validate_order(self, value):
        checkOrder(value)
        return value
    #Custom function to include both contents
    def get_contents(self, obj):
        text_contents = TextContent.objects.filter(module=obj)
        video_contents = VideoContent.objects.filter(module=obj)
        text_serializer = TextContentSerializer(text_contents, many=True)
        video_serializer = VideoContentSerializer(video_contents, many=True)
        # Return as a combined list of dictionaries
        return text_serializer.data + video_serializer.data

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True)
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'modules']
    #validate inputs at serializers
    def validate_title(self, value):
        return checkTitle(value)
    def validate_description(self, value):
        return checkDescription(value)
    def validate_updated_at(self, value):
        checkDate(value)
        return value