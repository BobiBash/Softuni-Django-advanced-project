from django.db import models

from accounts.models import PawMedicUser


# Create your models here.

class ForumPost(models.Model):
    author = models.ForeignKey(PawMedicUser, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()

class Comment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(PawMedicUser, on_delete=models.CASCADE, related_name='authored_comments')
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True)

