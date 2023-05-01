from .base import *
from dotenv import load_dotenv
import os

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Load the .env file
load_dotenv()

# Retrieve the FERNET_KEY from the environment
FERNET_KEY = os.environ.get('FERNET_KEY')