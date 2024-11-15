from rest_framework import serializers
from .models import Subject, Course, Module, TextContent, VideoContent, Content
from .helpers import checkDate,checkDescription,checkOrder,checkText,checkTitle
from django.contrib.contenttypes.models import ContentType
class TextContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextContent
        fields = '__all__'

class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    content_type = serializers.SlugRelatedField(
        queryset = ContentType.objects.filter(model__in=('textcontent', 'videocontent')),
        slug_field='model'
    )
    class Meta:
        model = Content
        fields = ['id', 'module', 'order', 'content_type', 'object_id', 'item']

    def get_item(self, obj):
        if isinstance(obj.item, TextContent):
            return TextContentSerializer(obj.item).data
        elif isinstance(obj.item, VideoContent):
            return VideoContentSerializer(obj.item).data
        return None

    def create(self, validated_data):
        content_data = self.initial_data.get('item')
        content_type = validated_data.pop('content_type')
        model_class = content_type.model_class()
        content_serializer_class = None

        if content_type.model == 'textcontent':
            content_serializer_class = TextContentSerializer
        elif content_type.model == 'videocontent':
            content_serializer_class = VideoContentSerializer
        else:
            raise serializers.ValidationError('Invalid content type')

        content_serializer = content_serializer_class(data=content_data)
        content_serializer.is_valid(raise_exception=True)
        content_instance = content_serializer.save(owner=self.context['request'].user)
        validated_data['object_id'] = content_instance.id
        validated_data['content_type'] = content_type

        return super().create(validated_data)

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
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"