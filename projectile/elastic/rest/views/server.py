from ...documents.server import ServerDocument
from ..serializers.server import ServerSearchSerializer

from projectile.elastic import ElasticSearchAPIView, ElasticSearchAfterPagination


class ServerSearchView(ElasticSearchAPIView):
    pagination_class = ElasticSearchAfterPagination
    serializer_class = ServerSearchSerializer

    def get(self, request, *args, **kwargs):
        search = ServerDocument.search()

        # sorting - required for search_after pagination
        search = search.sort("-created_at", "uid")

        # filtering via query params
        name = request.query_params.get("name")
        owner = request.query_params.get("owner_uid")

        if name:
            search = search.query("match", name=name)

        if owner:
            search = search.query("term", owner=owner)

        return self.paginate(request=request, search=search)
