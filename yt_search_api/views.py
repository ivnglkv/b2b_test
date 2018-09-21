from rest_framework import generics

from .models import SearchKeyword, YTVideo
from .pagination import MediumResultSetPagination
from .serializers import SearchKeywordSerializer, YTVideoSerializer


class SearchKeywordList(generics.ListCreateAPIView):
    queryset = SearchKeyword.objects.all()
    serializer_class = SearchKeywordSerializer


class SearchKeywordDetail(generics.RetrieveDestroyAPIView):
    queryset = SearchKeyword.objects.all()
    serializer_class = SearchKeywordSerializer


class YTVideoList(generics.ListAPIView):
    serializer_class = YTVideoSerializer
    pagination_class = MediumResultSetPagination

    def get_queryset(self):
        keyword_pk = self.kwargs['key_word']

        queryset = YTVideo.objects.filter(key_words__pk=keyword_pk)

        return queryset
