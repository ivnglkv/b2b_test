from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics
from rest_framework.exceptions import NotFound

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
        keyword_pk = self.kwargs['keyword_pk']

        # В случае, если ключевого слова с таким id не существует, вернуть 404
        # Иначе будет не отличить ответы в случаях, если к ключевому слову не найдены видео
        # и когда запрошенного ключевого слова не существует
        try:
            SearchKeyword.objects.get(pk=keyword_pk)
        except ObjectDoesNotExist:
            raise NotFound('Keyword not found')

        queryset = YTVideo.objects.filter(key_words__pk=keyword_pk)

        return queryset
