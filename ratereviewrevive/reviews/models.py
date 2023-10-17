from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

TEXT_SYMB_LIM = 30


class PublishedModel(models.Model):
    """Абстрактная модель. Добавляет дату публикации."""
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Slug', unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField('Slug', unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    description = models.CharField(max_length=256,
                                   verbose_name='Описание произведения',
                                   blank=True)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры произведения'
    )
    category = models.ForeignKey(
        Category,
        related_name='category_title',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class Review(PublishedModel):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='reviews')
    score = models.SmallIntegerField('Оценка',
                                     validators=(MinValueValidator(1),
                                                 MaxValueValidator(10)))

    def __str__(self):
        return self.text[:TEXT_SYMB_LIM]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review_from_one_user'
            )
        ]


class Comment(PublishedModel):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='comments')

    def __str__(self):
        return self.text[:TEXT_SYMB_LIM]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
