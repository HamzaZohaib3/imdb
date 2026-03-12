from django.db import models

# Create your models here.
class watchlist(models.Model):
    
    title = models.CharField(max_length=50)
    story_line = models.CharField(max_length=100)
    plateform = models.ForeignKey("streamplatform", on_delete=models.CASCADE, related_name= 'watch_list')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title
    
class streamplatform(models.Model):
    
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=100)
    website = models.URLField(max_length=200)


    def __str__(self):
        return self.name




