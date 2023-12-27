from django.db import models
from user.models import User
# Create your models here.

class Comment(models.Model):
    message = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
    

    def __str__(self):
        return str(self.id)


class ToDo(models.Model):
    class ColorListChoice(models.TextChoices):
        red = 'red', 'Red'
        blue = 'blue', 'Blue'
        green = 'green', 'Green'
        yellow = 'yellow', 'yellow'
        purple = 'purple', 'purple'
        orange = 'orange', 'orange'
        brown = 'brown', 'brown'
        pink = 'pink', 'pink'
        aqua = 'aqua', 'aqua'
        white = 'white', 'white'
    
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=20, choices=ColorListChoice.choices, blank=True)
    priority = models.IntegerField(default=0)
    hashtags = models.CharField(blank=True, max_length=300)
    comments = models.ManyToManyField(Comment, blank=True)
    description = models.CharField(max_length=300)
    # share
    

    class Meta:
        abstract=True


class ToDoItem(ToDo):
    start = models.DateTimeField(blank=True)
    end = models.DateTimeField(blank=True)
    completed = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='list/images/', null=True, blank=True)
    worker = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='worker')

    def __str__(self):
        return self.description


    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'


class ToDoList(ToDo):
    title = models.CharField(max_length=150)
    icon = models.ImageField(upload_to='list/images/', null=True, blank=True)
    point = models.FloatField(default=0)
    items = models.ManyToManyField(ToDoItem, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    
    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'list'
        verbose_name_plural = 'lists'