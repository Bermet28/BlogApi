# function based view
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Category, Post, Comments
from . import serializers
from .permissions import IsAuthor


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PostListSerializer
        return serializers.PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [permissions.IsAuthenticated(), IsAuthor()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return serializers.PostCreateSerializer
        return serializers.PostSerializer


class CommentsListCreateView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializers
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (permissions.AllowAny(),)
        return [permissions.IsAuthenticated(), IsAuthor]



# @api_view(['GET'])
# def category_list(request):
#     query_set = Category.objects.all()
#     serializer = serializers.CategorySerializer(query_set, many=True)
#     return Response(data=serializer.data, status=200)



# class Based view(APIview)


class CategoryListView(APIView):
    def get(self, request):
        queryset = Category.objects.all()
        serializer = serializers.CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)






