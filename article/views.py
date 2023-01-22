from .models import Article
from .serializers import ArticleSerializer

from rest_framework import generics

    
class ArticleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()


class ArticleDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()
    lookup_field='pk'
