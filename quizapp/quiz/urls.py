from django.urls import path
from . import views

app_name = 'quiz'


urlpatterns = [
    path('', views.quizapp_home, name='quizapp_home'),
    path('addquiz/', views.addquiz, name='addquiz'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('question/<int:question_id>/choices/', views.edit_choices, name='edit_choices'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    path('quiz/api/check_answer/<int:question_id>/', views.check_answer_api, name='check_answer_api'),
]