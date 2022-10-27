from django.db import models

# Create your models here.
class Tweet(models.Model):
    name = models.TextField(blank=False, null=False)
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True) #created_at

    def __str__(self):
        #return the tweet description
        return self.description