from rest_framework.serializers import ValidationError

def choice_validator(choices): 
    def validate_choice(value):
        valid_choices = [choice[0] for choice in choices]
        if value not in valid_choices:
            raise ValidationError(f'"{value}" is not one of the permitted values: {valid_choices}')
        return valid_choices
    return validate_choice
