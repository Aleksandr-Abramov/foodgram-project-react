from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Follow

from .serializers import (FollowCreateSerializer,
                          ShowFollowListUserSerializer, )

User = get_user_model()


class DockTemplate(TemplateView):
    template_name = 'docs/redoc.html'


class ShowListUserFollow(APIView):
    def get(self, request):
        user = self.request.user
        context = self.request
        queryset = User.objects.filter(following__user=user)

        serializer = ShowFollowListUserSerializer(queryset, many=True, context=context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowCreateDelete(APIView):
    def get(self, request, author_id):
        data = {
            "user": self.request.user.id,
            "author": author_id
        }
        serializer = FollowCreateSerializer(
            data=data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, author_id):
        user = self.request.user
        author = get_object_or_404(User, id=author_id)
        obj = get_object_or_404(Follow, user=user, author=author)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
