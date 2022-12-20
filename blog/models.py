from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Post status
STATUS = ((0, "Draft"), (1, "Published"))


# Post Model
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)

    # Order posts on created field (-: descending order)
    class Meta:
        ordering = ["-created_on"]

    # Return a string representation of an object
    def __str__(self):
        return self.title

    # Return the total number of likes on a post
    def number_of_likes(self):
        return self.likes.count()


# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80, unique=True)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    # Order posts on created field (-: descending order)
    class Meta:
        ordering = ["-created_on"]

    # Return a string representation of an object
    def __str__(self):
        return f"Comment {self.body} by {self.name}"
