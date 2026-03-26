from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Quiz, Question, Choice
from .forms import QuizForm, QuestionForm, ChoiceForm
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice, QuizAttempt
from django.db.models import Avg



def quizapp_home(request):
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'quiz/quizapp_home.html', {
        'active_page': 'home',
        'quizzes': quizzes,
    })

def addquiz(request):
    return render(request, 'quiz/addquiz.html', {'active_page': 'addquiz'})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('quiz:quizapp_home')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/register.html', {'form': form, 'active_page': 'register'})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('quiz:quizapp_home')
    else:
        form = AuthenticationForm()
    return render(request, 'quiz/login.html', {'form': form, 'active_page': 'login'})

def logout(request):
    auth_logout(request)
    return redirect('quiz:login')

def profile(request):
    created_quizzes = request.user.quizzes.all()
    attempts = request.user.quiz_attempts.all().order_by('-completed_at')
    return render(request, 'quiz/profile.html', {
        'active_page': 'profile',
        'created_quizzes': created_quizzes,
        'attempts': attempts,
    })


@login_required
def addquiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            return redirect('quiz:add_question', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'quiz/addquiz.html', {'form': form, 'active_page': 'addquiz'})


@login_required
def add_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id, created_by=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.order = quiz.questions.count() + 1
            question.save()

            if question.question_type == 'truefalse':
                Choice.objects.create(question=question, text='True', is_correct=False)
                Choice.objects.create(question=question, text='False', is_correct=False)
                return redirect('quiz:edit_choices', question_id=question.id)
            elif question.question_type == 'fillblank':
                return redirect('quiz:edit_choices', question_id=question.id)
            else:
                return redirect('quiz:edit_choices', question_id=question.id)
    else:
        form = QuestionForm()
    return render(request, 'quiz/add_question.html', {
        'form': form,
        'quiz': quiz,
    })


@login_required
def edit_choices(request, question_id):
    question = Question.objects.get(id=question_id, quiz__created_by=request.user)
    quiz = question.quiz

    if request.method == 'POST':
        if question.question_type == 'truefalse':
            correct = request.POST.get('correct')
            for choice in question.choices.all():
                choice.is_correct = (choice.text == correct)
                choice.save()
            return redirect('quiz:add_question', quiz_id=quiz.id)

        elif question.question_type == 'fillblank':
            answer = request.POST.get('answer', '').strip()
            question.choices.all().delete()
            Choice.objects.create(question=question, text=answer, is_correct=True)
            return redirect('quiz:add_question', quiz_id=quiz.id)

        else:
            question.choices.all().delete()
            texts = request.POST.getlist('choice_text')
            correct_idx = request.POST.get('correct')
            for i, text in enumerate(texts):
                if text.strip():
                    Choice.objects.create(
                        question=question,
                        text=text.strip(),
                        is_correct=(str(i) == correct_idx)
                    )
            return redirect('quiz:add_question', quiz_id=quiz.id)

    return render(request, 'quiz/edit_choices.html', {
        'question': question,
        'quiz': quiz,
    })

def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})


def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        score = 0
        total = questions.count()
        results = []

        for question in questions:
            if question.question_type == 'fillblank':
                user_answer = request.POST.get(f'question_{question.id}', '').strip()
                correct = question.choices.filter(is_correct=True).first()
                is_correct = correct and user_answer.lower() == correct.text.lower()
            else:
                user_answer = request.POST.get(f'question_{question.id}')
                correct = question.choices.filter(is_correct=True).first()
                is_correct = correct and str(correct.id) == user_answer

            if is_correct:
                score += 1

            results.append({
                'question': question,
                'user_answer': user_answer,
                'correct_answer': correct,
                'is_correct': is_correct,
            })

        if request.user.is_authenticated:
            QuizAttempt.objects.create(
                user=request.user,
                quiz=quiz,
                score=score,
                total=total,
            )

        return render(request, 'quiz/quiz_results.html', {
            'quiz': quiz,
            'results': results,
            'score': score,
            'total': total,
            'percentage': round(score / total * 100) if total > 0 else 0,
        })

    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'questions': questions,
    })




@login_required
def quiz_results(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id, created_by=request.user)
    attempts = quiz.attempts.all().order_by('-completed_at')
    avg = attempts.aggregate(avg=Avg('score'))['avg'] or 0
    total = quiz.questions.count()
    avg_score = round(avg / total * 100) if total > 0 else 0
    return render(request, 'quiz/quiz_results.html', {
        'quiz': quiz,
        'attempts': attempts,
        'avg_score': avg_score,
    })