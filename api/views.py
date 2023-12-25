from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListCreateAPIView, UpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from .mylib.serializers import UserSerializer, ListSerializer
from .mylib.permissions import IsAuthentication, IsAuthenticatedAuthor
from .mylib.filters import ToDoListFilter
from .mylib.paginations import CustomPagination
from todo.models import ToDoList
from django_filters import rest_framework as filters


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
    permission_classes = [IsAuthentication]
    authentication_classes = [BasicAuthentication, TokenAuthentication, ]
    pagination_class = CustomPagination
    queryset = ToDoList.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ToDoListFilter


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ListManager(RetrieveUpdateDestroyAPIView):
    serializer_class = ListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedAuthor]
    lookup_field = 'slug'
    queryset = ToDoList