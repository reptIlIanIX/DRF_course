from datetime import timedelta

from django.db import models

from DRF_course import settings

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    DAILY = 'ежедневно'
    WEEKLY = 'еженедельно'

    PERIODS = ((DAILY, 'ежедневно'),
               (WEEKLY, 'еженедельно'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    name = models.CharField(max_length=100, verbose_name='название привычки')
    place = models.CharField(max_length=100, **NULLABLE, verbose_name='место выполнения привычки')
    time = models.TimeField(**NULLABLE, verbose_name='время выполнения привычки')
    action = models.CharField(max_length=100, verbose_name='действие привычки')
    good_habit = models.BooleanField(default=True, verbose_name='признак приятной привычки')
    connected_habit = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE,
                                        verbose_name='связанная привычка')
    period = models.CharField(max_length=20, choices=PERIODS, default=DAILY,
                              verbose_name='периодичность привычки')
    duration = models.DurationField(default=timedelta(minutes=2),
                                    verbose_name='продолжительность выполнения привычки')
    public_habit = models.BooleanField(default=True, verbose_name='признак публичной привычки')
    prize = models.CharField(max_length=100, verbose_name='вознаграждение', **NULLABLE)