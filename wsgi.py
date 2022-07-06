import os
from dotenv import load_dotenv
load_dotenv('.env')
python_path = os.environ.get('PYTHON_PATH')
os.system(f'export PYTHONPATH={python_path}')
from application import app as application
