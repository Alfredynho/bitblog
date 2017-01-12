# -*- encoding:utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from rest_framework import status as status_code
from rest_framework.response import Response


class DoneResponse(Response):
    """
    Base class for REST Exceptions based on CEH from @vicobox.
    """
    def __init__(self, detail=None, code=None, status=None):
        response = dict()
        if detail:
            response["detail"] = detail
        else:
            response["detail"] = _("Operación exitosa !")
        if status:
            scode = status
        else:
            scode = status_code.HTTP_200_OK
        if code:
            response["code"] = code
        super(DoneResponse, self).__init__(data=response, status=scode)