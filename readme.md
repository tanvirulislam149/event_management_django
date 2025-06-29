# Event Nest - Event Management Website

A Event management for organizing different events at different locations for making people's special day memorable

## Live Website

[Click here to visit the live site](https://event-management-django.onrender.com/)

## Credentials

- User Credentials

        username: shuvo
        password: asdfasdf12

- Organizer Credentials

        username: tanvir
        password: asdfasdf12

- Admin Credentials

        username: admin
        password: admin

## Features

- Member registration and login
- User, Organizer and Admin dashboard for gym management
- Send email on event confirm
- Managing events
- Mobile-responsive UI

## Tech Stack

**Frontend & Backend:**

- Django

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/tanvirulislam149/event_management_django
cd event_management_django

# Create a virtual environment
python -m venv gym_env

# Activate the virtual environment
# On Windows:
env\Scripts\activate

# On macOS/Linux:
source env/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

```bash
# For Sending Email
EMAIL_BACKEND=your_EMAIL_BACKEND
EMAIL_HOST=your_EMAIL_HOST
EMAIL_USE_TLS=your_EMAIL_USE_TLS
EMAIL_PORT=your_EMAIL_PORT
EMAIL_HOST_USER=your_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=your_EMAIL_HOST_PASSWORD

FRONTEND_URL=your_FRONTEND_URL
```

**Deployment:**

- Render (Frontend & Backend)
