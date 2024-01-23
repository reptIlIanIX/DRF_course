from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Привычки """

    class Meta:
        model = Habit
        fields = '__all__'

        validators = [
            validator_for_habit,
        ]
