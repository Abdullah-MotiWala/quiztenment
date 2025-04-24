import os
import sys

# Adjust the paths correctly based on yours
sys.path.insert(0, '/new_quiztainment_1')  # replace with your actual project path
sys.path.insert(0, os.path.dirname(__file__))  # this ensures current directory is included

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz.settings')  # Set the correct project name

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()