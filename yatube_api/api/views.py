from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework import filters

from .serializers import *
from .permissions import OwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return Comment.objects.filter(
            post=post
        )
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class FollowViewSet(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    pagination_class = None

    def get_queryset(self):
        return Follow.objects.filter(
            user=self.request.user
        )
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request):
        user = request.user
        try:
            following = User.objects.get(
                username=request.data.get('following')
            )
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if user == following \
            or Follow.objects.filter(user=user, following=following).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().create(request)
