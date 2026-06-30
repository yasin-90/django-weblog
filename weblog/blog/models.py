from django.db import models


# Create your models here.
class User(models.Model):
    user =models.CharField(max_length=30)
    password =models.IntegerField(max_length=30)

    def __str__(self):
        return f"{self.user}"


class Category(models.Model):
    name =models.CharField(max_length=30)
    slug =models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name =models.CharField(max_length=30)
    slug =models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"
    

class Post(models.Model):
    title =models.CharField(max_length=30)
    slug =models.CharField(max_length=30)
    body =models.TextField(max_length=500)
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    category =models.ManyToManyField(Category)
    tags =models.ManyToManyField(Tag)
    published =models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True,  editable=False)
    

    def __str__(self):
        return f"{self.title} {self.category} {self.tags}"
    
class comment(models.Model):
        post=models.ForeignKey(Post,on_delete=models.CASCADE)
        author=models.CharField(max_length=30)
        body =models.TextField(max_length=500)
        created_at = models.DateTimeField(auto_now=True, editable=False)
        def __str__(self):
            return f"{self.author}"
        
