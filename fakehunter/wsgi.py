from dj_static import Cling
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fakehunter.settings')

application = Cling(get_wsgi_application())
