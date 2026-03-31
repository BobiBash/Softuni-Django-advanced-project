from django.db import models

# Create your models here.

class ForumPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

class Comment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True)

