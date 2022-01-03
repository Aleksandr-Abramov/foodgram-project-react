from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import IngredientFilter, RecipeFilter, TagsFilter
from .models import (Favorite, Follow, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .permissions import AdminOrAuthorOrReadOnly
from .serializers import (FavoriteSerializer, FollowCreateSerializer,
                          IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          ShowFollowUserListOrDetailSerializer, TagsSerializer)

User = get_user_model()


class DockTemplate(TemplateView):
    template_name = 'docs/redoc.html'


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TagsFilter


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = IngredientFilter


class FavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, recipe_id):
        user = self.request.user.id
        recipe = recipe_id
        data = {
            "user": user,
            "recipe": recipe
        }
        serializer = FavoriteSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        obj = get_object_or_404(Favorite, user=user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, recipe_id):
        user = self.request.user.id
        recipe = recipe_id
        data = {
            "user": user,
            "recipe": recipe
        }
        context = {"request": request}
        serializer = ShoppingCartSerializer(
            data=data,
            context=context,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        obj = get_object_or_404(ShoppingCart, user=user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartDownloadsAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_shopping_list = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user).values_list(
            'ingredient__name', 'amount', 'ingredient__measurement_unit')
        all_count_ingredients = user_shopping_list.values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            total=Sum('amount')).order_by('-total')
        ingredients_list = []
        for ingredient in all_count_ingredients:
            ingredients_list.append(
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["total"]} '
                f'{ingredient["ingredient__measurement_unit"]} \n'
            )
        return HttpResponse(ingredients_list, {
            'content_type': 'text/plain',
            'Content-Disposition': 'attachment; filename="shopping_list.txt"'
        })


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [AdminOrAuthorOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        method = self.request.method
        if method == "GET":
            return RecipeSerializer
        return RecipeCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class ShowListUserFollow(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShowFollowUserListOrDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)

    def get_serializer_context(self):
        context = self.request
        return context


class FollowCreateDelete(APIView):
    permission_classes = [IsAuthenticated, ]

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
