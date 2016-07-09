"""
nodeshot custom exceptions
"""
from rest_framework import status
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response


class WarpResponse(Response):
    """
    Base class for REST Exceptions based on CEH from @jvacx.
    """
    def __init__(self, message=None, code=None, status_code=None, docs=None, dev_message=None ):
        response = dict()
        if message:
            response["message"] = message
        else:
            response["message"] = _("Missing arguments !")

        if status_code:
            scode = status_code
        else:
            scode = status.HTTP_400_BAD_REQUEST

        if code:
            response["code"] = code

        if docs:
            response["docs"] = docs

        if dev_message:
            response["dev_message"] = dev_message

        super(WarpResponse, self).__init__(data=response, status=scode)
