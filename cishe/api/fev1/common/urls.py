from django.urls import path

from cishe.api.fev1.common.views import get_model_field_values


urlpatterns = [
    path("model-field-values/", get_model_field_values, name="model_field_value"),
]
