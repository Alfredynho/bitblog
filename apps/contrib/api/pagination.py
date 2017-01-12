# -*- encoding:utf-8 -*-

from rest_framework import pagination
from rest_framework.response import Response


class LinkHeaderPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()

        headers = dict()
        if next_url is not None:
            headers["Page-Next"] = "%s" % next_url
        else:
            headers["Page-Next"] = "null"

        if previous_url is not None:
            headers["Page-Prev"] = "%s" % previous_url
        else:
            headers["Page-Prev"] = "null"

        if next_url is not None or previous_url is not None:
            headers["Paginated"] = "true"
            headers["Page-Size"] = self.get_page_size(data)

        return Response(data, headers=headers)