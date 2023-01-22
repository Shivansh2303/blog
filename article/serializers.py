from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.timezone import now

from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    title=serializers.CharField(required=True,validators=[UniqueValidator(queryset=Article.objects.all())])
    content=serializers.CharField(allow_blank=True)
    # created=serializers.DateTimeField(read_only=True)

    class Meta:
        model=Article
        fields='__all__'
    