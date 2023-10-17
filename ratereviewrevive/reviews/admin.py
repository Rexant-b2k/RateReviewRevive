from django.contrib import admin

from reviews.models import Category, Genre, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category'
    )
    search_fields = ('id', 'name')
    list_display_links = ('id', 'name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    search_fields = ('id', 'name')
    list_display_links = ('id', 'name')


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    search_fields = ('id', 'name')
    list_display_links = ('id', 'name')


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
