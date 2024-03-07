# movies/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        # Generate slug from the name
        self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='posters/')
    description = models.TextField()
    release_date = models.DateField()
    actors = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=True, null=False)
    trailer_link = models.URLField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    average_rating = models.FloatField(default=0)
    link=models.SlugField()

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()
    # def __str__(self):
    #     return self.User

