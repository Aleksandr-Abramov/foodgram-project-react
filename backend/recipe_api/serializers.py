from rest_framework import serializers

from .models import (Follow,
                     User,
                     Recipe,
                     RecipeIngredient,
                     Ingredient,
                     Tag)
from users.serializers import UserDetailSerializer


# сериализация для Tags

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "color",
            "slug",
        )


# сериализация для Recipe

class RecipeUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=self.context.get("request").user,
            author=obj
        ).exists()


class ShowIngredientsInRecipe(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(source="ingredient.measurement_unit")

    class Meta:
        model = RecipeIngredient
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    author = RecipeUserSerializer(many=False)
    tags = TagsSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "text",
            "cooking_time",
        )

    def get_ingredients(self, obj):
        data = RecipeIngredient.objects.filter(recipe=obj)
        return ShowIngredientsInRecipe(data, many=True).data


class RecipeCreateIngridientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = (
            "id",
            "amount"
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeCreateIngridientSerializer(many=True)
    author = RecipeUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "ingredients",
            "tags",
            "author",
            "name",
            "text",
            "cooking_time",
        )

    def validate_tags(self, tags):
        sum_tags = self.initial_data.get("tags")
        len_tags = len(sum_tags)
        if len_tags == 0:
            raise serializers.ValidationError("Пожалуйста, добавте минимум 1 тэг.")
        if len_tags > len(set(sum_tags)):
            print(set(sum_tags))
            raise serializers.ValidationError("Теги не должны повторятся")
        return tags

    def validate(self, data):
        ingredients = self.initial_data.get("ingredients")
        if not ingredients:
            raise serializers.ValidationError("Пожалуйста, добавте минимум 1 ингридиент.")
        for ingridient in ingredients:
            if int(ingridient["amount"]) <= 0:
                raise serializers.ValidationError("Количество должно быть положительным!")
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise serializers.ValidationError('Время готовки не может быть'
                                              ' отрицательным числом или нулем!')
        return data

    def create(self, validated_data):
        author = self.context["request"].user
        data_ingredients = validated_data.pop("ingredients")
        data_tags = validated_data.pop("tags")
        new_recipe = Recipe.objects.create(**validated_data, author=author)

        for tag in data_tags:
            new_recipe.tags.add(tag)
        for ingridient in data_ingredients:
            new_recipe.ingredients.add(ingridient["id"])
            RecipeIngredient.objects.create(
                recipe=new_recipe,
                ingredient=ingridient["id"],
                amount=ingridient["amount"]
            )
        return new_recipe

    def update(self, recipe, validated_data):
        author = self.context["request"].user

        recipe.author = author
        recipe.text = validated_data.get("text", recipe.text)
        recipe.name = validated_data.get("name", recipe.name)
        recipe.cooking_time = validated_data.get("cooking_time", recipe.cooking_time)
        if "tags" in self.initial_data:
            data_tags = validated_data.pop("tags")
            recipe.tags.set(data_tags)
        if "ingredients" in self.initial_data:
            data_ingredients = validated_data.pop("ingredients")
            recipe.ingredients.clear()
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            for ingredient in data_ingredients:
                ingredient_id = ingredient['id']
                amount = ingredient['amount']

                RecipeIngredient.objects.update_or_create(
                    recipe=recipe, ingredient=ingredient_id,
                    defaults={"amount": amount})
                recipe.ingredients.add(ingredient_id)
        recipe.save()
        return recipe

    def to_representation(self, instance):
        data = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data


# cериализация для Follow


# class ShowFollowListUserSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField()
#     recipes_count = serializers.SerializerMethodField()
#     recipes = serializers.SerializerMethodField()
#     class Meta:
#         model = User
#         fields = (
#             "email",
#             "id",
#             "username",
#             "first_name",
#             "last_name",
#             "is_subscribed",
#             "recipes",
#             "recipes_count",
#         )
#
#     def get_is_subscribed(self, obj):
#         user = self.context.user.id
#         return Follow.objects.filter(user=user, author=obj.id).exists()
#
#     def get_recipes(self, obj):
#         return ShowFollowRecipeUserSerializer(obj.recipes.all(), many=True).data
#     def get_recipes_count(self, obj):
#         return obj.recipes.count()

class ShowFollowRecipeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "cooking_time",
        )


class ShowFollowUserListOrDetailSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        user = self.context.user
        author = obj
        return Follow.objects.filter(
            user=user,
            author=author
        ).exists()

    def get_recipes(self, obj):
        return ShowFollowRecipeUserSerializer(obj.recipes.all(), many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = (
            "user",
            "author",
        )

    def validate(self, data):
        method = self.context.get("request").method
        user = data["user"].id
        author = data["author"].id
        follow_exist = Follow.objects.filter(
            user__id=user, author__id=author
        ).exists()

        if method == "GET":
            if user == author or follow_exist:
                print(follow_exist)
                raise serializers.ValidationError(
                    ("Подписка уже существует."
                     "Оформить подписку на самого себя, невозможно")
                )
        Follow.objects.create(
            user=data["user"],
            author=data["author"]
        )
        return data

    def to_representation(self, instance):
        context = self.context.get("request")

        return ShowFollowUserListOrDetailSerializer(
            instance["author"],
            context=context
        ).data
