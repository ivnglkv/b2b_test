from rest_framework import serializers
from .models import SearchKeyword, YTVideo


class SearchKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchKeyword
        fields = ('id', 'key_word')


class YTVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YTVideo
        fields = ('id', 'title', 'url', 'published_at')
