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

