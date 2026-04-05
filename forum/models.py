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


# class Vote(models.Model):
#     post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='votes')
#     type = models.CharField(choices=ForumVoteType.choices, max_length=10)
#     user = models.ForeignKey(PawMedicUser, on_delete=models.CASCADE, related_name='user_votes')
#
#     class Meta:
#         unique_together = ('post', 'user')