import os
import sys
from dotenv import load_dotenv
load_dotenv('.env')
sys.path.append(os.environ.get('PYTHON_PATH'))
from application import app as application
