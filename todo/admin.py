from django.contrib import admin
from .models import ToDoList, ToDoItem, Comment
# Register your models here.

admin.site.register(ToDoList)
admin.site.register(ToDoItem)
admin.site.register(Comment)