from typing import Any

from rest_framework.response import Response


class ElasticSearchAfterPagination:
    """
    we use ES to both serve list data, instead of Model.objects.all() and also for searching
    search_after needs the search = Document.search() to be sorted

    1: we start from 0, and go up to page size and return all the items in between
    and also return the last item's speicific fields which were used to sort the doc,

    2: we do the next search/request with query params like this:
    search_after_date=1747581038734
    search_after_uid=61a33459-45cb-420c-bb65-56f9e9c4fe22

    3: this means that ES will now do what its best known for. Search.
    it will search the sorted document and find the item with those sort values and
    starts returning the next page from there.
    so for whichever item, item.created_at = search_after_date and item.uid = search_after_uid
    will be the first item in the page
    and and it will give us 'n' items if page_size = n
    """

    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 500

    def __init__(self):
        self.results: list = []
        self.search_after: dict = {}

    def _parse_pagination_params(self, request):
        params = request.query_params

        try:
            size: int = min(
                int(params.get("page_size", self.DEFAULT_PAGE_SIZE)),
                self.MAX_PAGE_SIZE,
            )
        except ValueError:
            size = self.DEFAULT_PAGE_SIZE

        search_after_date: str = params.get("search_after_date")
        search_after_uid: str = params.get("search_after_uid")

        pagination_params = {
            "size": size,
            "search_after_date": search_after_date,
            "search_after_uid": search_after_uid,
        }

        return pagination_params

    def paginate_queryset(self, request, search) -> list[Any]:
        pagination_params = self._parse_pagination_params(request)

        size, search_after_date, search_after_uid = (
            pagination_params["size"],
            pagination_params["search_after_date"],
            pagination_params["search_after_uid"],
        )

        query = search.params(from_=0, size=size)

        if search_after_date and search_after_uid:
            query = query.params(search_after=[search_after_date, search_after_uid])

        self.results = list(query)
        return self.results

    def get_paginated_response(self, data):
        if self.results and hasattr(self.results[-1].meta, "sort"):
            last_hit = list(self.results[-1].meta.sort)
            self.search_after = {"date": last_hit[0], "uid": last_hit[1]}

        return Response(
            {
                "count": len(data),
                "search_after": self.search_after,  # pass in next request as params
                "results": data,
            }
        )
