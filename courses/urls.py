from django.urls import path
from .views import (
    user_list_view,
    course_detail_view
    )

app_name = 'courses'

urlpatterns = [
    path('', user_list_view, name='home'),
    path('courses/<pk>/', course_detail_view, name='detail'),
]