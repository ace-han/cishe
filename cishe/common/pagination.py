from typing import cast

from django.utils.functional import SimpleLazyObject
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings


class StandardPageNumberPagination(PageNumberPagination):
    """Doing this class only to make page_size work."""

    page_size_query_param = "page_size"


def prepare_paginator(pagination_class) -> PageNumberPagination:
    return pagination_class()


paginator = cast(
    PageNumberPagination,
    SimpleLazyObject(lambda: prepare_paginator(api_settings.DEFAULT_PAGINATION_CLASS)),
)


def prepare_pagination_response(qs, request, view=None) -> Response:
    """For api_view functions exclusively."""
    page = paginator.paginate_queryset(qs, request, view)
    if page is not None:
        return paginator.get_paginated_response(page)
    return Response(qs)
