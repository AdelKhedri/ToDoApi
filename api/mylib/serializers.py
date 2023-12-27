from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .validators import username_validator, password_validator, exist_user
from rest_framework.exceptions import ValidationError
from todo.models import ToDoList, ToDoItem, Comment


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

    class Meta:
        model = Comment
        fields = ['message', 'author', 'id']


class ListSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    author = serializers.CharField(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = ToDoList
        fields = ['title','color','priority','hashtags','comments','description','icon','items', 'slug', 'created', 'updated', 'author']