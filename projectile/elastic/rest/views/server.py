from ...documents.server import ServerDocument
from ..serializers.server import ServerSearchSerializer

from elastic import ElasticSearchAPIView, ElasticSearchAfterPagination


class ServerSearchView(ElasticSearchAPIView):
    pagination_class = ElasticSearchAfterPagination
    serializer_class = ServerSearchSerializer

    def get(self, request, *args, **kwargs):
        name = request.query_params.get("name")
        owner = request.query_params.get("owner_uid")
        order = request.query_params.get("order")

        search = ServerDocument.search()

        # sorting - required for search_after pagination
        timestamp_ordering = "created_at" if order == "ASC" else "-created_at"
        search = search.sort(timestamp_ordering, "uid")

        # filtering via query params
        if name:
            search = search.query("match", name=name)

        if owner:
            search = search.query("term", owner=owner)

        return self.paginate(request=request, search=search)
