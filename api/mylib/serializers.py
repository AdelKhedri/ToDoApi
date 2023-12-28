from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .validators import username_validator, password_validator, exist_user
from rest_framework.exceptions import ValidationError
from todo.models import ToDoList, ToDoItem, Comment
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(validators = [password_validator], write_only=True)
    invaited_by = serializers.CharField(validators = [exist_user])
    username = serializers.CharField(validators = [username_validator, UniqueValidator(queryset=get_user_model().objects.all(), message='V: this username already used for another user')],
                                     error_messages = {
                                         'required': 'username filed is required.',
                                         'blank': 'username field can not be blank.'
                                     })
    email = serializers.EmailField(validators = [UniqueValidator(queryset=get_user_model().objects.all(), message='V: this email aleady user for another user')],
                                   error_messages = {
                                         'required': 'email filed is required.',
                                         'blank': 'email field can not be blank.'
                                    })
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'invaited_by']

    
    def create(self, validated_data):
        invaited = get_user_model().objects.get(username=validated_data.pop('invaited_by'))
        user = super().create(validated_data)
        user.set_password(validated_data.pop('password'))
        user.invaited_by = invaited
        user.save()
        return user
    


# class ChangePasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(write_only=True)
#     new_password = serializers.CharField(validators = [password_validator], write_only=True)

#     def validate(self, data):
#         if not 
#         # if data['password'] != data['password2']:
#             raise ValidationError('password1 not match with password2')

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)

    def create(self, validated_data):
        request = self.context['request']
        instance = super().create(validated_data)
        instance.author=request.user
        instance.save()
        return instance
    

    class Meta:
        model = Comment
        fields = ['message', 'author', 'id']


class ItemSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(allow_unicode=True)
    author = serializers.CharField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True, required=False) # for create comment when ceate item set read_only=False
    worker = serializers.CharField(allow_null=True, required=False)


    def create(self, validated_data):
        # comments = validated_data.pop('comments')
        user = self.context['request'].user

        # if need to add comment when createing item
        # comments_saved = []
        # for comment in comments:
        #     comment_instance = Comment.objects.create(**comment, author=user)
        #     comments_saved.append(comment_instance)
        
        item = ToDoItem.objects.create(**validated_data, author=user)
        # item.comments.set(comments_saved)
        # item.save()
        return item
    
    
    def update(self, instance, validated_data):
        username = validated_data.get('worker', None)
        if username is not None :
            worker1 = get_object_or_404(get_user_model(), username=username)
            instance.worker = worker1
        else:
            instance.worker = None
        
        instance.slug = validated_data.pop('slug', instance.slug)
        instance.color = validated_data.pop('color', instance.color)
        instance.priority = validated_data.pop('priority', instance.priority)
        instance.hashtags = validated_data.pop('hashtags', instance.hashtags)
        instance.description = validated_data.pop('description', instance.description)
        instance.start = validated_data.pop('start', instance.start)
        instance.end = validated_data.pop('end', instance.end)
        instance.completed = validated_data.pop('completed', instance.completed)
        instance.icon = validated_data.pop('icon', instance.icon)
        instance.save()
        return instance
    
    class Meta:
        model = ToDoItem
        fields = ['slug', 'comments', 'color', 'priority', 'hashtags', 'description', 'start', 'end', 'completed', 'icon', 'worker', 'author']


class ListSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    author = serializers.CharField(read_only=True)
    items = ItemSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = ToDoList
        fields = ['title','color','priority','hashtags','comments','description','icon','items', 'slug', 'created', 'updated', 'author']