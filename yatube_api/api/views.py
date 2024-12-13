from api.permissions import IsOwnerOrReadOnly
from api.serializers import (CommentSerializer, GroupSerializer,
                                   PostSerializer)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Comment, Group, Post


class BaseVievSet(viewsets.ModelViewSet):
    """Базовый вьюсет."""

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return Response({
                'detail': 'У вас нет прав на редактирование'})
        return super().update(request, *args, **kwargs)

    def portial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return Response({
                'detail': 'У вас нет прав на редактирование'})
        return super().update(request, *args, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для API постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для API групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьсет для API комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['post_id'])
        serializer.save(post=post, author=self.request.user)
