from rest_framework import generics

from .models import SearchKeyword
from .serializers import SearchKeywordSerializer


class SearchKeywordList(generics.ListCreateAPIView):
    queryset = SearchKeyword.objects.all()
    serializer_class = SearchKeywordSerializer


class SearchKeywordDetail(generics.RetrieveDestroyAPIView):
    queryset = SearchKeyword.objects.all()
    serializer_class = SearchKeywordSerializer
