from rest_framework.decorators import action
from rest_framework.response import Response


class BulkDeleteMixin(object):
    @action(detail=False, methods=("post",), url_path="bulk-delete")
    def bulk_delete(self, request):
        qs = self.get_queryset()
        # filter_queryset just filters on query_params
        filtered = self.filter_queryset(qs)
        # count = filtered.count()
        count, _ = filtered.delete()
        return Response({"detail": "{} deleted".format(count)})
