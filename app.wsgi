import sys

activate_this = '/home/season/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

sys.path.insert(0,'/var/www/html/Amazon-SP-API')
from app import app as application