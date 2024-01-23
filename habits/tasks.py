from celery import shared_task
from celery.worker.state import requests

from DRF_course import settings
from DRF_course.settings import TELEGRAM_BOT_API_KEY, TELEGRAM_CHAT_ID
from habits.models import Habit

bot_token = TELEGRAM_BOT_API_KEY
telegram_id = TELEGRAM_CHAT_ID
get_id_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

@shared_task
def message_to_bot(habit_pk):
    habit = Habit.objects.get(id=habit_pk)
    requests.get(url=f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_API_KEY}/sendMessage',
                 params={'chat_id': habit.user.telegram_id,
            'text': f'Привет {habit.user}! Время {habit.time}. Пора идти в {habit.place} и сделать {habit.action}. ' \
                    f'Это займет {habit.duration} минут!'
        }
    )