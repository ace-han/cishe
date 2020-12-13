from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    comment = models.TextField()
    commented_by = models.CharField(max_length=64)
    submitted_at = models.DateTimeField(auto_now_add=True, null=True)
    removed = models.BooleanField(default=False)
