from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import json


def validate_json(string):
    try:
        json_object = json.loads(string)
        return False
    except ValueError as e:
        return True
