import csv
import os

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from ratereviewrevive.settings import BASE_DIR
from reviews import models
from users.models import User


class Command(BaseCommand):

    def read_csv(self, filename, func):
        with open(filename) as f:
            reader = csv.DictReader(f)
            func(self, reader)

    def create_users(self, reader):
        for row in reader:
            User.objects.get_or_create(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )

    def create_categories(self, reader):
        for row in reader:
            models.Category.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )

    def create_genres(self, reader):
        for row in reader:
            models.Genre.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )

    def create_titles(self, reader):
        for row in reader:
            category = get_object_or_404(models.Category, id=row['category'])
            models.Title.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=category
            )

    def create_genre_title(self, reader):
        for row in reader:
            title = get_object_or_404(models.Title, id=row['title_id'])
            genre = get_object_or_404(models.Genre, id=row['genre_id'])
            title.genre.add(genre)

    def create_reviews(self, reader):
        for row in reader:
            title = get_object_or_404(models.Title, id=row['title_id'])
            author = get_object_or_404(User, id=row['author'])
            models.Review.objects.get_or_create(
                id=row['id'],
                title=title,
                text=row['text'],
                author=author,
                score=row['score'],
                pub_date=row['pub_date']
            )

    def create_comments(self, reader):
        for row in reader:
            review = get_object_or_404(models.Review, id=row['review_id'])
            author = get_object_or_404(User, id=row['author'])
            models.Comment.objects.get_or_create(
                id=row['id'],
                review=review,
                text=row['text'],
                author=author,
                pub_date=row['pub_date']
            )

    DATA_FILES = {
        'users.csv': create_users,
        'category.csv': create_categories,
        'genre.csv': create_genres,
        'titles.csv': create_titles,
        'genre_title.csv': create_genre_title,
        'review.csv': create_reviews,
        'comments.csv': create_comments
    }

    def _create_data(self):
        file = 'genre.csv'
        for file, func in self.DATA_FILES.items():
            path_to_file = os.path.join(BASE_DIR, 'static', 'data', file)
            self.read_csv(path_to_file, func)
            print(f'import {file} completed')

    def handle(self, *args, **options):
        self._create_data()
