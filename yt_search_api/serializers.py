from rest_framework import serializers
from .models import SearchKeyword, YTVideo


class SearchKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchKeyword
        fields = ('id', 'word')


class YTVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YTVideo
        fields = ('title', 'url', 'date', 'key_words')
