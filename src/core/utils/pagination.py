import math

from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    # page_size = 20
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        self.page_size = int(self.request.query_params.get('size'))
        data = super(CustomPagination, self).get_paginated_response(data)
        data.data['page_number'] = math.ceil(data.data.get('count') / self.page_size)
        data.data['page_size'] = self.page_size
        if self.page.has_next():
            data.data['next_page_number'] = self.page.next_page_number()
        else:
            data.data['next_page_number'] = None
        return data
