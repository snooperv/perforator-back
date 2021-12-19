from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(GradeCategory)
admin.site.register(PerformanceReview)
admin.site.register(Review)
admin.site.register(Grade)
admin.site.register(AverageGrade)

@admin.register(SelfReview)
class SelfReviewAdmin(admin.ModelAdmin):
    pass

