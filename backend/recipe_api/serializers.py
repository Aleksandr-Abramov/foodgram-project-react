from rest_framework import serializers

from .models import (Follow,
                     User,
                     )
from users.serializers import UserDetailSerializer


# cериализация для Follow

class ShowFollowListUserSerializer(serializers.ModelSerializer):
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
            # "recipes",
            # "recipes_count",
        )

    def get_is_subscribed(self, obj):
        user = self.context.user.id
        return Follow.objects.filter(user=user, author=obj.id).exists()


class ShowFollowUserDetailSerializer(serializers.ModelSerializer):
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
            # "recipes",
            # "recipes_count",
        )

    def get_is_subscribed(self, obj):
        user = self.context.user
        author = obj
        return Follow.objects.filter(
            user=user,
            author=author
        ).exists()


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

        return ShowFollowUserDetailSerializer(
            instance["author"],
            context=context
        ).data
