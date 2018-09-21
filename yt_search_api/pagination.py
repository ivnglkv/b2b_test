from rest_framework.pagination import PageNumberPagination


class MediumResultSetPagination(PageNumberPagination):
    page_size = 10
