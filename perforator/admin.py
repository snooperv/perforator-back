from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Review)


@admin.register(SelfReview)
class SelfReviewAdmin(admin.ModelAdmin):
    pass

