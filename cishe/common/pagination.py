from rest_framework.pagination import PageNumberPagination


class StandardPageNumberPagination(PageNumberPagination):
    """Doing this class only to make page_size work."""

    page_size_query_param = "page_size"
