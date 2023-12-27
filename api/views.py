from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView, ListCreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from .mylib.serializers import UserSerializer, ListSerializer, CommentSerializer
from .mylib.permissions import IsAuthenticated, IsAuthenticatedAuthor
from .mylib.filters import ToDoListFilter
from .mylib.paginations import CustomPagination
from todo.models import ToDoList, ToDoItem, Comment
from django_filters import rest_framework as filters
from django.db.models import F


class UserSinupApi(CreateAPIView):
    serializer_class = UserSerializer

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response('this method is not allowd')


# class UserChangePasswordApi(UpdateAPIView):
#     serializer_class = ChangePasswordSerializer
#     permission_classes = [IsSelf,]
#     authentication_classes = [TokenAuthentication,]

#     def get_object(self):
#         obj = self.request.user
#         return obj


class ListCreateListApi(ListCreateAPIView):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, TokenAuthentication, ]
    pagination_class = CustomPagination
    queryset = ToDoList.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ToDoListFilter


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ListManagerApi(RetrieveUpdateDestroyAPIView):
    serializer_class = ListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedAuthor]
    lookup_field = 'slug'
    queryset = ToDoList


class CreateCommentApi(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,] # for all users
    authentication_classes = [TokenAuthentication]
    queryset = Comment
    

    # only author can add comment to lists command this function and any one can  add comment to all lists!
    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(request)
            user = request.user
            list_instance = get_object_or_404(ToDoList, pk=self.kwargs['pk'])
            if user != list_instance.author:
                self.permission_denied(request, "only author can add comment to a list")


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        list_instance = get_object_or_404(ToDoList, pk=self.kwargs['pk'])
        list_instance.comments.add(serializer.instance)
        list_instance.save()
        # print(serializer.instance.id) # with out id in serializer
        


class DeleteCommentApi(DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedAuthor,]
    authentication_classes = [TokenAuthentication]
    queryset = Comment