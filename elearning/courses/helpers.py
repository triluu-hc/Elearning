from rest_framework import serializers

def checkTitle(title):
    title = title.strip().capitalize()
    if len(title) < 5:
        raise serializers.ValidationError("Title must be between 5 and 255 characters")
    for char in title:
        if not (char.isalnum() or char.isspace()):
            raise serializers.ValidationError("Title must not contain special characters.")
    return title 

def checkDescription(description):
    description = description.strip().capitalize()
    if len(description) < 30:
        raise serializers.ValidationError("Description must be at least 30 characters.")
    for char in description:
        if not (char.isalnum() or char.isspace()):
            raise serializers.ValidationError("Description must not contain special characters.")
    return description

def checkDate(created_at, updated_at):
    if created_at and updated_at and created_at > updated_at:
        raise serializers.ValidationError("Created time must be before updated time")

def checkOrder(order):
    if order < 1 or order > 100:
        raise serializers.ValidationError("Order must be positive lower than 100")
     
def checkText(text):
    text = text.strip().capitalize()
    if len(text) < 30:
        raise serializers.ValidationError("Text must be at least 30 characters.")
    return text
        