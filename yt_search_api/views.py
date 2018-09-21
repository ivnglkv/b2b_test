from rest_framework import generics

from .models import SearchKeyword, YTVideo
from .serializers import SearchKeywordSerializer, YTVideoSerializer


class SearchKeywordList(generics.ListCreateAPIView):
    queryset = SearchKeyword.objects.all()
    serializer_class = SearchKeywordSerializer


class SearchKeywordDetail(generics.RetrieveDestroyAPIView):
    queryset = SearchKeyword.objects.all()
    serializer_class = SearchKeywordSerializer


class YTVideoList(generics.ListAPIView):
    queryset = YTVideo.objects.all()
    serializer_class = YTVideoSerializer
