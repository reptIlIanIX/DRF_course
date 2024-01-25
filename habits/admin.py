from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):

    list_display = ('name', 'public_habit', 'user',)
    list_filter = ('name',)
    search_fields = ('name',)