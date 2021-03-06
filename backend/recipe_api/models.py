from django.contrib.auth import get_user_model
from django.db import models

from .validators import greater_than_zero, validation_hex

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Имя ингредиента"
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единица измерения"
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Имя тега"
    )
    color = models.CharField(
        max_length=7,
        verbose_name="цвет",
        validators=[validation_hex]
    )
    slug = models.SlugField(
        verbose_name="слаг"
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name="tags",
        verbose_name="Теги"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="автор")
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="ingredients",
        verbose_name="Ингредиенты"
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название рецепта"
    )
    image = models.ImageField(
        upload_to="recipes/",
        verbose_name="Изображение",
    )
    text = models.TextField(
        verbose_name="Описание рецепта"
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[greater_than_zero]
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return f'{self.name} {self.author}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент"
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        default=1,
        validators=[greater_than_zero]

    )

    class Meta:
        verbose_name = "Ингредиенты в рецептах"
        verbose_name_plural = "Ингредиенты в рецептах"

    def __str__(self):
        return "Ингредиент в рецепте"


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="unique_follow"
            )
        ]

    def __str__(self):
        return f'{self.user} following {self.author}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="favorite_user"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="favorite_recipe"
    )

    added_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = "Избранные"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_favorite"
            )
        ]

    def __str__(self):
        return f"{self.user} added {self.recipe}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Пользователь"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Рецепт"
    )

    added_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = verbose_name
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_shopping_cart')]

    def __str__(self):
        return f'{self.user} added {self.recipe}'
