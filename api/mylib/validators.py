from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from user.models import User


def username_validator(value):
    pattern = re.compile(r'[a-zA-Z0-9_.]')
    username_len = len(value)
    if username_len < 4:
        raise ValidationError(_('V: username must be equal 5 character or more than of 5 character'))
    elif username_len > 150:
        raise ValidationError(_('V: username must be equal 150 character or less than 150 character'))
    if value[0].isnumeric():
        raise ValidationError(_('V: username can not start with number'))
    if not pattern.match(value):
        raise ValidationError(_('V: username can only contains _ . numbers and charcters'))
    

def password_validator(value):
    if value.isnumeric():
        raise ValidationError(_('password must contains characters'))
    elif value.isalpha():
        raise ValidationError(_('password must contains numbers'))
    elif len(value) < 8:
        raise ValidationError(_('password must be more than of 7 ckaracters'))
    

def exist_user(value):
    try:
        User.objects.get(username=value)
        pass
    except User.DoesNotExist:
        raise ValidationError(_('user not found'))