from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .models import Follow, Recipe, RecipeIngredient


from .serializers import (FollowCreateSerializer,
                          ShowFollowUserListOrDetailSerializer,
                          RecipeSerializer,
                          ShowIngredientsInRecipe,
                          RecipeCreateSerializer)
User = get_user_model()


class DockTemplate(TemplateView):
    template_name = 'docs/redoc.html'


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        method = self.request.method
        if method == "GET":
            return RecipeSerializer
        return RecipeCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context




class ShowListUserFollow(APIView):
    def get(self, request):
        user = self.request.user
        context = self.request
        queryset = User.objects.filter(following__user=user)
        serializer = ShowFollowUserListOrDetailSerializer(queryset, many=True, context=context)

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
