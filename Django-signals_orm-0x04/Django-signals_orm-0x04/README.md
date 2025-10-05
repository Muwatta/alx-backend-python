# Django Signals and ORM Project

This project is part of the ALX Backend Python curriculum (Django-signals_orm-0x04). It implements a messaging system using Django, focusing on signals, ORM queries, and caching.

## Features
- **Task 0**: Sends notifications when a message is created using Django signals.
- **Task 1**: Logs message edit history with a `MessageHistory` model.
- **Task 2**: Cleans up user-related data (messages, notifications, histories) on user deletion.
- **Task 3**: Displays threaded conversations using a self-referential `Message` model.
- **Task 4**: Custom manager (`UnreadMessagesManager`) for filtering unread messages.
- **Task 5**: Caches message list view for 60 seconds.

## Setup
1. Clone the repository: `git clone <repo-url>`
2. Navigate to `Django-signals_orm-0x04/messaging_app/`
3. Activate virtual environment: `source venv/Scripts/activate`
4. Install dependencies: `pip install -r ../requirements.txt`
5. Run migrations: `python manage.py makemigrations messaging && python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`
8. Access at `http://127.0.0.1:8000/admin/` or `/messages/<receiver_id>/`

## Testing
- Run tests: `python manage.py test messaging`
- Tests cover signal-based notifications, edit history, and user deletion cleanup.

## Author
Muwatta