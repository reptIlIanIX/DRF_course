from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


# Create your tests here.
class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='reptilianix@gmail.com', is_active=True)
        self.user.set_password('12345')
        self.user.save()

        self.client.force_authenticate(user=self.user)

    def test_create(self):
        get_token = reverse('users:token_obtain_pair')
        token_response = self.client.post(path=get_token, data={'email': 'reptilianix@gmail.com', 'password': '12345'})
        token = token_response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
        data_habit = {'user': self.user.pk,
                      'name': 'Test',
                      'action': 'Test',
                      "good_habit": True,
                      'period': "еженедельно"}

        response = self.client.post(reverse('habits:create'), data=data_habit)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.json(), {'id': 1, 'user': 1, 'name': 'Test', 'place': None, 'time': None,
                                            'action': 'Test', 'good_habit': True, 'period': 'еженедельно',
                                            'duration': '00:02:00',
                                            'public_habit': False, 'connected_habit': None, 'prize': None})
        self.assertTrue(Habit.objects.all().exists())

    def test_list(self):
        self.maxDiff = None

        get_token = reverse('users:token_obtain_pair')
        token_response = self.client.post(path=get_token, data={'email': 'reptilianix@gmail.com', 'password': '12345'})
        token = token_response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        Habit.objects.create(
            user=self.user,
            name='Test',
            action='Test',
            good_habit=True,
            period='ежедневно',
        )
        response = self.client.get(reverse("habits:list"))

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.json(),
                          {'count': 1, 'next': None, 'previous': None,
                           'results': [{'id': 1, 'user': 1,
                                        'name': 'Test', 'place': None,
                                        'time': None, 'action': 'Test',
                                        'good_habit': True,
                                        'period': 'ежедневно',
                                        'duration': '00:02:00',
                                        'public_habit': True, 'connected_habit': None,
                                        'prize': None}]})

    def test_detail(self):
        get_token = reverse('users:token_obtain_pair')
        token_response = self.client.post(path=get_token, data={'email': 'reptilianix@gmail.com', 'password': '12345'})
        token = token_response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        habit = Habit.objects.create(
            user=self.user,
            name='Test',
            action='Test',
            good_habit=True,
            period='ежедневно'
        )
        response = self.client.get(
            reverse('habits:detail', kwargs={'pk': habit.pk})
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'id': 1, 'user': 1, 'name': 'Test', 'place': None, 'time': None,
             'action': 'Test', 'good_habit': True, 'period': 'ежедневно', 'duration': '00:02:00',
             'public_habit': True, 'connected_habit': None, 'prize': None}
        )

    def test_change(self):

        # отправляем запрос на аутентификацию пользователя
        get_token = reverse('users:token_obtain_pair')
        token_response = self.client.post(path=get_token,
                                          data={'email': 'reptilianix@gmail.com', 'password': '12345'})
        token = token_response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # создаем тестовую привычку
        habit = Habit.objects.create(
            user=self.user,
            name='Test',
            action='Test',
            good_habit=True,
            period='ежедневно'
        )

        # данные для изменения привычки
        data_habit_change = {
            'name': 'Test_1',
        }

        # получаем детали привычки
        response = self.client.patch(
            reverse('habits:update', kwargs={'pk': habit.pk}),
            data=data_habit_change
        )

        print(response.json())

        # проверяем ответ на получение привычки
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # проверяем ответ на соответствие сохраненных данных
        self.assertEquals(
            response.json(),
            {'id': 1, 'user': 1, 'name': 'Test_1', 'place': None, 'time': None,
             'action': 'Test', 'good_habit': True, 'period': 'ежедневно', 'duration': '00:02:00',
             'public_habit': True, 'connected_habit': None, 'prize': None}
        )

    def test_delete(self):

        # отправляем запрос на аутентификацию пользователя
        get_token = reverse('users:token_obtain_pair')
        token_response = self.client.post(path=get_token,
                                          data={'email': 'reptilianix@gmail.com', 'password': '12345'})
        token = token_response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # создаем тестовую привычку
        habit = Habit.objects.create(
            user=self.user,
            name='Test',
            action='Test',
            good_habit=True,
            period='ежедневно'
        )

        # получаем детали привычки
        response = self.client.delete(
            reverse('habits:delete', kwargs={'pk': habit.pk})
        )

        # проверяем ответ на получение привычки
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
