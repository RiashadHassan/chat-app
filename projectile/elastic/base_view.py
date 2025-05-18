from rest_framework.views import APIView
from rest_framework.response import Response


class ElasticSearchAPIView(APIView):
    pagination_class = None
    serializer_class = None

    def paginate(self, request, search):
        if self.pagination_class is None:
            raise ValueError(
                f"{self.__class__.__name__} class must include a 'pagination_class' attribute"
            )
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(request, search)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # fallback (should never hit)
        serializer = self.serializer_class(search.execute(), many=True)
        return Response(serializer.data)
