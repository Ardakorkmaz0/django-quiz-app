from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    RESULT_MODE_CHOICES = [
        ('instant', 'Instant'),
        ('end', 'End of Quiz'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    result_mode = models.CharField(max_length=10, choices=RESULT_MODE_CHOICES, default='end')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=160, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('multiple', 'Multiple Choice'),
        ('truefalse', 'True/False'),
        ('fillblank', 'Fill in the Blank'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='multiple')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts', null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    def percentage(self):
        if self.total == 0:
            return 0
        return round(self.score / self.total * 100)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}/{self.total})"