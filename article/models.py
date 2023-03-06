from django.db import models
from django.utils import timezone
from user.models import UserModel

class Article(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    # is_published= models.BooleanField(default=False)
    owner=models.ForeignKey(UserModel,related_name='posts',on_delete=models.CASCADE)

    
    def __str__(self):
        return self.title
    