from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.timezone import now
from rest_framework.reverse import reverse


from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    owner=serializers.HyperlinkedRelatedField(view_name="user-detail",lookup_field='pk',read_only=True)
    # owner=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Article
        fields=['id','title','content','created_at','updated_at','owner']
    
    def create(self, validated_data):
        return Article.objects.create(**validated_data)
    
    # def validate(self, attrs):
    #     request=self.context.get('request')
    #     user=request.user
    #     qs=Article.objects.filter(title__iexact=title)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"<{title}> is aleady a post title.")
    #     return attrs
    
    
    # def get_owner(self,obj):
    #     request=self.context.get("request")
    #     print(__file__,request)
    #     if request in None:
    #         return None
    #     return reverse("user-detail",args=[obj.pk],request=request)