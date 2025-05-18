from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, BasePagination


class ElasticPagination(PageNumberPagination):
    page_size = 500
    max_page_size = 1000
    page_size_query_param = "page_size"


class ElasticSearchAfterPagination(BasePagination):
    page_size = 10

    def paginate_queryset(self, results, request, view=None):
        self.request = request
        self.size = int(request.query_params.get("size", self.page_size))
        self.search_after = request.query_params.getlist("search_after")

        self.query = results.extra(from_=0, size=self.size)

        if self.search_after:
            self.query = self.query.extra(search_after=self.search_after)

        self.results = list(self.query)
        return self.results

    def get_paginated_response(self, data):
        if self.results:
            last_hit = self.results[-1].meta.sort
        else:
            last_hit = None

        return Response(
            {
                "results": data,
                "search_after": last_hit,  # this should be passed in next request
                "count": len(data),
            }
        )
