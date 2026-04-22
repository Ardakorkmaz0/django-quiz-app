# Django Quiz App

A simple and interactive quiz application built with Django. Users can create custom quizzes, add different types of questions, and take quizzes created by others.

## Features

- **User Authentication:** Register, Login, and Logout functionality.
- **User Profiles:** Manage personal information and profile picture.
- **Create Quizzes:** Build custom quizzes with titles and descriptions.
- **Question Types:** Supports Multiple Choice, True/False, and Fill in the Blank questions.
- **Take Quizzes:** Take quizzes and view your score instantly or at the end.
- **Quiz Results:** Track past quiz attempts and scores.

## Technologies Used

- Python
- Django
- SQLite
- HTML/CSS

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ardakorkmaz0/django-quiz-app.git
   cd django-quiz-app
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django
   ```

4. **Run database migrations:**
   ```bash
   cd quizapp
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

6. Open `http://127.0.0.1:8000/` in your web browser.
