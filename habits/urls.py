from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitListAPIView, HabitCreateAPIView, HabitPublicListAPIView, HabitDestroyAPIView, \
    HabitUpdateAPIView, HabitRetrieveAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('', HabitListAPIView.as_view(), name='habits'),
    path('create/', HabitCreateAPIView.as_view(), name='create'),
    path('public/', HabitPublicListAPIView.as_view(), name='public'),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name='detail'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='update'),
    path('delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='delete'),
]
