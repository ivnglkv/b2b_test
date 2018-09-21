from rest_framework import serializers
from .models import SearchKeyword


class SearchKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchKeyword
        fields = ('id', 'word')
