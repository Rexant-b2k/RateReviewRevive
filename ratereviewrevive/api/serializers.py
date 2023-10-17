import datetime as dt

from django.db.models import Q
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import (UniqueTogetherValidator,
                                       UniqueValidator,
                                       ValidationError)

from reviews import models
from users.models import User

THE_OLDEST_TITLE = -2200


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'email', 'bio', 'role',)
        model = User


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=100,
    )
    email = serializers.EmailField(
        max_length=254,
    )

    class Meta:
        fields = ('username', 'email',)
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(f'Имя пользователя: {value} недоступно')
        return value

    def validate(self, attrs):
        username = self.initial_data.get('username')
        email = self.initial_data.get('email')
        if User.objects.filter(Q(email=email) & ~Q(username=username)
                               | ~Q(email=email) & Q(username=username)
                               ).exists():
            raise serializers.ValidationError(
                'Username или email уже занят'
            )
        return attrs


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


# Самым древним литературным произведением является
# "Эпос о Гильгамеше"(также поэма "О всём видавшем"),
# шедевр и главное достояние аккадской литературы.
# Его создание большинство учёных относят к 22 веку до нашей эры
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        exclude = ['id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        exclude = ['id']


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')
        model = models.Title
        read_only_fields = ['id', 'rating']
        # Сделал проверку уникальности произведения в сочетании название-год
        # Ведь может быть переиздание произведения, которое также называется
        validators = [
            UniqueTogetherValidator(
                queryset=models.Title.objects.all(),
                fields=('name', 'year')
            )
        ]

    def validate_year(self, value):
        year = dt.datetime.now().year
        if not (THE_OLDEST_TITLE < value <= year):
            raise serializers.ValidationError('Проверьте год произведения!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = models.Review

    def validate(self, attrs):
        request = self.context.get('request')
        if request.method == 'POST':
            title = self.context.get('view').kwargs.get('title_id')
            if models.Review.objects.filter(author=request.user,
                                            title=title).exists():
                raise serializers.ValidationError(
                    'Нельзя оставлять более одного отзыва!'
                )
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = models.Comment
