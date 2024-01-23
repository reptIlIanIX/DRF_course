from django.shortcuts import render
from rest_framework import generics


# Create your views here.
class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]