from django_celery_beat.models import CrontabSchedule

from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask

from datetime import datetime

import pytz

from DRF_course import settings
from habits.models import Habit
from habits.tasks import telegram_id, message_to_bot


def check_habits_daily():

    date_time_now = datetime.now()
    moscow_timezone = pytz.timezone('Europe/Moscow')
    date_now = date_time_now.astimezone(moscow_timezone)
    time_now = date_now.time()

    habits = Habit.objects.filter(time__hour=time_now.hour, time__minute=time_now.minute,
                                  period='ежедневно', good_habit=False)

    for habit in habits:
        create_message(habit.id)


def check_habits_weekly():

    date_time_now = datetime.now()
    moscow_timezone = pytz.timezone('Europe/Moscow')
    date_now = date_time_now.astimezone(moscow_timezone)
    time_now = date_now.time()

    habits = Habit.objects.filter(time__hour=time_now.hour, time__minute=time_now.minute,
                                  period='еженедельно', good_habit=False)

    for habit in habits:
        create_message(habit.id)


def create_message(habit_id):

    habit = Habit.objects.get(id=habit_id)

    user = habit.user
    time = habit.time
    action = habit.action
    place = habit.place
    duration = round(habit.duration.total_seconds() / 60)

    message = f'Привет {user}! Время {time}. Пора идти в {place} и сделать {action}. ' \
              f'Это займет {duration} минут!'

    response = message_to_bot(telegram_id, message)
    if habit.connected_habit:
        good_habit_id = habit.connected_habit.id
        good_habit = Habit.objects.get(id=good_habit_id)
        nice_time = round(good_habit.duration.total_seconds() / 60)
        message = (f'Молодец! Ты выполнил {action}, за это тебе подарок {good_habit.action} '
                   f'в течение {nice_time} минут')

        time.sleep(10)
        nice_response = message_to_bot(telegram_id, message)
        return HttpResponse(nice_response)

    return HttpResponse(response)


# def create_reminder(habit):
#
#     crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
#         minute=habit.time.minute,
#         hour=habit.time.hour,
#         day_of_week='*' if habit.period == 'ежедневно' else '*/7',
#         month_of_year='*',
#         timezone=settings.TIME_ZONE
#     )
#
#     PeriodicTask.objects.create(
#         crontab=crontab_schedule,
#         name=f'Habit Task - {habit.name}',
#         task='habits.tasks.send_message_to_bot',
#         args=[habit.id],
#     )


def delete_reminder(habit):

    task_name = f'send_message_to_bot_{habit.id}'
    PeriodicTask.objects.filter(name=task_name).delete()


def update_reminder(habit):

    delete_reminder(habit)
    create_reminder(habit)
