import importlib

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from cishe.common.pagination import prepare_pagination_response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_model_field_values(request):
    """Return model field's distinct values."""
    model_class_path = request.query_params.get("model_class_path")
    model_field_path = request.query_params.get("model_field_path")
    values = (request.query_params.get("value") or "").split(",")
    class_module_path, class_name = model_class_path.rsplit(".", 1)

    module = importlib.import_module(class_module_path)
    ModelClass = getattr(module, class_name)
    qs = ModelClass.objects.values_list(model_field_path, flat=True).distinct()
    if len(values) < 2:
        if values[0]:
            qs = qs.filter(**{f"{model_field_path}__icontains": values[0]})
    else:
        qs = qs.filter(**{f"{model_field_path}__in": values})
    return prepare_pagination_response(qs, request)
