from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api import serializers
from api.filters import TitleFilter
from api.permissions import (IsAdmin,
                             IsAdminOrReadOnly,
                             IsModeratorAuthorAdminOrReadOnly)
from api.viewsets import ListCreateDestroyViewSet
from reviews import models
from users.models import User


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = models.Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('id')
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        category = get_object_or_404(
            models.Category, slug=self.request.data.get('category')
        )
        genre = models.Genre.objects.filter(
            slug__in=MultiValueDict(self.request.data).getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        serializer.save()
        category = get_object_or_404(
            models.Category, slug=self.request.data.get('category')
        )
        genre = models.Genre.objects.filter(
            slug__in=MultiValueDict(self.request.data).getlist('genre')
        )
        serializer.save(category=category, genre=genre)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsModeratorAuthorAdminOrReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(models.Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(models.Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsModeratorAuthorAdminOrReadOnly,)

    def perform_create(self, serializer):
        review = get_object_or_404(models.Review,
                                   id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(models.Review,
                                   id=self.kwargs.get('review_id'))
        return review.comments.all()


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    queryset = User.objects.all()
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = request.user

        if request.method == 'PATCH':
            serializer = serializers.UserSerializer(user,
                                                    data=request.data,
                                                    partial=True)
            if serializer.is_valid():
                serializer.save(role=user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    serializer = serializers.CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    user, created = User.objects.get_or_create(
        email=email,
        username=username
    )

    token = default_token_generator.make_token(user)
    send_confirmation_email(email, token)

    return Response(serializer.data, status=status.HTTP_200_OK)


def send_confirmation_email(email, token):
    subject = 'Регистрация на RateReviewRevive'
    message = f'Код подтверждения: {token}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


@api_view(['POST'])
def check_token(request):
    serializer = serializers.TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        jwt_token = AccessToken.for_user(user)
        return JsonResponse(({'token': str(jwt_token)}),
                            status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
