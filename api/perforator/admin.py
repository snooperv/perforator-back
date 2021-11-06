from django.contrib import admin
from .models import SelfReview


@admin.register(SelfReview)
class SelfReviewAdmin(admin.ModelAdmin):
    list_display = ('input_part', 'plans')

