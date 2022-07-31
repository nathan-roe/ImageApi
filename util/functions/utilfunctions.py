import base64
from io import BytesIO
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler
from util.models import ExpiringToken


def get_uid(request):
    return request.META.get('HTTP_AUTHORIZATION').split()[1]


def token_to_uid(request):
    """
    Function for simplifying token to user_profile association
    """
    # Assigning UserProfile object associated with authenticated Token
    # get token straight from headers
    try:
        tok = request.META.get('HTTP_AUTHORIZATION').split()
        cur_token = ExpiringToken.objects.get(key=tok[1])
        has_expired = ExpiringToken.expired(cur_token)
        if not has_expired:
            return cur_token.user
        else:
            return
    except ExpiringToken.DoesNotExist:
        return


# Formats B64 to a File object for s3 image CRUD
def b64_to_fileobj(file):
    _, imgstr = file.split(';base64,')
    bf_data = base64.b64decode(imgstr)
    return  BytesIO(bf_data)


def encode_string_to_b64(target_string):
    """
    Encodes target string to a Base64 object, using UTF-8 encoding
    """
    slug_bytes = target_string.encode('utf-8')
    b64_string = base64.b64encode(slug_bytes)
    return b64_string.decode('utf-8')


def decode_b64_to_string(target_b64):
    """
    Decodes target Base64 object to a human readable string, using UTF-8 encoding
    """
    b64_bytes = target_b64.encode('utf-8')
    slug_bytes = base64.b64decode(b64_bytes)
    return slug_bytes.decode('utf-8')


def custom_view_exception_handler(exc, context):
    """
    Function that works directly with DRF and is registered in settings.py
    Inherits the default DRF exception handling and adds logging and custom
    exception handling outside of default 500
    """

    # Call DRF default exception handler first
    response = exception_handler(exc, context)

    # Checks if the raised exception is of the type you want to handle
    if isinstance(exc, KeyError):
        err_data = {'error': 'Invalid query parameter'}
        response = Response(err_data, status=status.HTTP_400_BAD_REQUEST)

    elif isinstance(exc, ValueError):
        err_data = {'error': 'Invalid request data'}
        response = Response(err_data, status=status.HTTP_400_BAD_REQUEST)

    elif isinstance(exc, ValidationError):
        err_data = {'error': 'Invalid form data, did not meet validation criteria'}
        response = Response(err_data, status=status.HTTP_400_BAD_REQUEST)

    elif isinstance(exc, ObjectDoesNotExist):
        err_data = {'error': 'Object not found'}
        response = Response(err_data, status=status.HTTP_404_NOT_FOUND)

    # Returns either DRF Response or None
    return response
