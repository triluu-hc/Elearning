from django.core.exceptions import ValidationError

def checkTitle(title):
    title = title.strip().capitalize()
    if len(title) < 5 or len(title) > 255:
        raise ValidationError("Title must be between 5 and 255 characters long.")
    for char in title:
        if not (char.isalnum() or char.isspace()):
            raise ValidationError("Title must not contain special characters.")
    return title 

def checkDescription(description):
    description = description.strip().capitalize()
    if len(description) < 30:
        raise ValidationError("Description must be at least 30 characters.")
    for char in description:
        if not (char.isalnum() or char.isspace()):
            raise ValidationError("Title must not contain special characters.")
    return description

def checkDate(created_at, updated_at):
    if created_at and updated_at and created_at > updated_at:
        raise ValidationError("Created time must be before updated time")

def checkOrder(order):
    if order > 100:
        raise ValidationError("Order must be lower than 100")
     
def checkText(text):
    text = text.strip().capitalize()
    if len(text) < 30:
        raise ValidationError("Description must be at least 30 characters.")
    return text
        