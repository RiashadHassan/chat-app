from rest_framework.response import Response
from rest_framework.views import APIView
from ...documents.server import ServerDocument
from ...pagination import ElasticPagination
from ..serializers.server import ServerSearchSerializer

from elasticsearch.helpers import scan
from elasticsearch_dsl import connections
from elasticsearch_dsl import Q


# class ServerSearchView(APIView):
#     pagination_class = ElasticPagination
#     serializer_class = ServerSearchSerializer

#     def get(self, request, *args, **kwargs):
#         es = connections.get_connection()

#         # scan retrieves *all* documents (deep pagination)
#         docs = scan(
#             client=es,
#             index=ServerDocument._index._name,
#             query={"query": {"match_all": {}}},
#         )

#         # scan returns generator of raw ES dicts
#         data = [doc["_source"] for doc in docs]  # '_source' is the actual document

#         # paginate the raw list of dicts
#         paginator = self.pagination_class()
#         page = paginator.paginate_queryset(data, request, view=self)

#         if page is not None:
#             serializer = self.serializer_class(page, many=True)
#             return paginator.get_paginated_response(serializer.data)

#         serializer = self.serializer_class(data, many=True)
#         return Response(serializer.data)


# class ServerSearchView(APIView):
#     pagination_class = ElasticPagination
#     serializer_class = ServerSearchSerializer
#     document = ServerDocument

#     def get_full_index(self):
#         es = connections.get_connection()
#         docs = scan(
#             client=es,
#             index=self.document._index._name,
#             query={"query": {"match_all": {}}},
#         )

#     def get(self, request, *args, **kwargs):
#         search = ServerDocument.search()
#         print(request.query_params)
#         # full text search
#         q = request.query_params.get("q")
#         if q:
#             search = search.query(
#                 "multi_match", query=q, fields=["name", "description"]
#             )

#         # field filters (owner_username=riashad-hassan)
#         owner_username = request.query_params.get("owner_username")
#         if owner_username:
#             search = search.filter("term", owner__username=owner_username)

#         # sorting (e.g. ?sort=name or ?sort=-created_at)
#         sort = request.query_params.get("sort")
#         if sort:
#             search = search.sort(sort)

#         response = search.execute()
#         results = [hit.to_dict() for hit in response]

#         paginator = self.pagination_class()
#         page = paginator.paginate_queryset(results, request, view=self)

#         if page is not None:
#             serializer = self.serializer_class(page, many=True)
#             return paginator.get_paginated_response(serializer.data)

#         serializer = self.serializer_class(results, many=True)
#         return Response(serializer.data)

from elasticsearch_dsl import Search
from django_elasticsearch_dsl.registries import registry

class ServerSearchView(APIView):
    pagination_class = ElasticPagination
    serializer_class = ServerSearchSerializer

    def get(self, request, *args, **kwargs):
        es = connections.get_connection()

        # Elasticsearch pagination
        page_number = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))
        from_ = (page_number - 1) * page_size

        search = {
            "from": from_,
            "size": page_size,
            "query": {
                "match_all": {}
            }
        }

        response = es.search(index=ServerDocument._index._name, body=search)
        data = [doc["_source"] for doc in response["hits"]["hits"]]

        serializer = self.serializer_class(data, many=True)
        return Response({
            "count": response["hits"]["total"]["value"],
            "results": serializer.data
        })
