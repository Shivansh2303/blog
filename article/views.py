from .models import Article
from .serializers import ArticleSerializer
from mindRetreats.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response

from rest_framework import permissions 
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework import generics

    
class ArticleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ArticleDetailUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=ArticleSerializer
    queryset=Article.objects.all()
    permission_classes=[permissions.IsAuthenticated,IsOwnerOrReadOnly]
    lookup_field='pk'
    
    # def retrieve(self, request,*args,**kwargs):
    #     instance=self.get_queryset()
    #     serializer=self.serializer_class(instance,context={'request':request})
    #     print(serializer.data)
    #     return Response(serializer.data)
