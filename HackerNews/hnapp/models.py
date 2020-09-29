from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField("HeadLine", max_length=256, unique=True)
    creator = models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    url = models.URLField("URL", max_length=256,blank=True)
    description = models.TextField("Description", blank=True)
    votes = models.IntegerField(null=True)
    comments = models.IntegerField(null=True)    

    def __unicode__(self):
        return self.title

    def count_votes(self):
        self.votes = Vote.objects.filter(post = self).count()
    
    def count_comments(self):
        self.comments = Comment.objects.filter(post = self).count()



class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __unicode__(self):
        return f"{self.user.username} upvoted {self.link.title}" 


class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    identifier = models.IntegerField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    def __unicode__(self):
        return f"Comment by {self.user.username}"
'''
class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()

    def __unicode__(self):
        return f"Comment by {self.user.username}"
'''
 
'''
class UserInfo(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return f"{self.user.username}"

class PostsInfo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    votes = models.IntegerField()
    comments = models.IntegerField()

    def count_votes(self):
        self.votes = Vote.objects.filter(post = self.post).count()
    
    def count_comments(self):
        self.comments = Comment.objects.filter(post = self.post).count()
'''


