from django.contrib import admin
from .models import Category, Movie, Review

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_release_date', 'get_category', 'added_by', 'display_average_rating')

    def get_release_date(self, obj):
        return obj.release_date

    def get_category(self, obj):
        return obj.category

    def display_average_rating(self, obj):
        return obj.average_rating

    get_release_date.admin_order_field = 'release_date'
    get_category.admin_order_field = 'category'
    display_average_rating.admin_order_field = 'average_rating'

admin.site.register(Category)
class categogryAdmin(admin.ModelAdmin):
        prepopulated_fields={'slug':('Category',)}
admin.site.register(Review)
admin.site.register(Movie, MovieAdmin)