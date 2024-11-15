from rest_framework import serializers
from .models import Subject, Course, Module, TextContent, VideoContent, Content
from .helpers import checkDate,checkDescription,checkOrder,checkText,checkTitle
from django.contrib.contenttypes.models import ContentType
class TextContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextContent
        fields = ['id', 'text']

    def create(self, validated_data):
        # Set any required fields, such as 'owner' if applicable
        # validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)



class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = ['id', 'video_url']

    def create(self, validated_data):
        # Set any required fields
        return super().create(validated_data)

class ContentSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'module', 'order', 'content_type', 'object_id', 'item']
        read_only_fields = ['module', 'order', 'content_type', 'object_id', 'item']

    def get_item(self, obj):
        if isinstance(obj.item, TextContent):
            return TextContentSerializer(obj.item).data
        elif isinstance(obj.item, VideoContent):
            return VideoContentSerializer(obj.item).data
        return None


class ModuleSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    course = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'course', 'title', 'description', 'order', 'contents']

    # Override the create method
    def create(self, validated_data):
        course = self.context['course']
        validated_data['course'] = course
        return super().create(validated_data)
    #validate inputs at serializers
    def validate_title(self, value):
        return checkTitle(value)
    def validate_description(self, value):
        return checkDescription(value)
    def validate_order(self, value):
        checkOrder(value)
        return value
    #Custom function to include both contents
    

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True) 
    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        required=False  
    )
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'description', 'created_at', 'updated_at', 'modules']
    #validate inputs at serializers
    def validate_title(self, value):
        return checkTitle(value)
    def validate_description(self, value):
        return checkDescription(value)
    def validate_updated_at(self, value):
        checkDate(value)
        return value
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"