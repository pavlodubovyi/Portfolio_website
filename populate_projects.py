import os
import django

# Django shell settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from projects.models import Project

# Deleting old projects in order not to duplicate
Project.objects.all().delete()

# List of projects
projects_data = [
    {
        "title": "REST API Contact List",
        "description": "FastAPI-based REST API with full CRUD functionality for managing contacts. "
                       "Implemented authentication, password reset, and caching with Redis. "
                       "Uses PostgreSQL and SQLAlchemy for data storage. "
                       "Has birthday reminders for the upcoming 7 days. "
                       "Integrated Cloudinary for avatar updates.",
        "stack": "FastAPI, PostgreSQL, SQLAlchemy, Redis, Cloudinary",
        "link": "https://github.com/pavlodubovyi"
    },
    {
        "title": "Django-based Quotes Website",
        "description": "Django-based web application to store and display famous quotes and author information. "
                       "Implemented user authentication, pagination, and PostgreSQL integration.",
        "stack": "Django, PostgreSQL",
        "link": "https://github.com/pavlodubovyi"
    },
    {
        "title": "Relational Database for a University",
        "description": "Relational database for a university/school. "
                       "Manages data of students, teachers, subjects, groups, and grades. "
                       "Written on Python 3.11, using SQLAlchemy.",
        "stack": "PostgreSQL, Python 3.11, SQLAlchemy",
        "link": "https://github.com/pavlodubovyi"
    }
]

# Adding projects to the DB
for project in projects_data:
    Project.objects.create(**project)

print("✅ Projects successfully added to the database!")
