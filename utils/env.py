import os
from dotenv import load_dotenv
load_dotenv()

PORT = int(os.environ.get('PORT'))
POSTGRES_PORT = int(os.environ.get('PGPORT'))
POSTGRES_USER = str(os.environ.get('POSTGRES_USER'))
POSTGRES_PASSWORD = str(os.environ.get('POSTGRES_PASSWORD'))
POSTGRES_DB = str(os.environ.get('POSTGRES_DB'))
DJANGO_SECRET_KEY = str(os.environ.get('DJANGO_SECRET_KEY'))
HUGGINGFACE_API_KEY = str(os.environ.get('HUGGINGFACE_API_KEY'))
HUGGINGFACE_MODEL = str(os.environ.get('HUGGINGFACE_MODEL'))
TELEGRAM_BOT_TOKEN = str(os.environ.get('TELEGRAM_BOT_TOKEN'))
GROQ_API_KEY = str(os.environ.get('GROQ_API_KEY'))
GROQ_CHAT_MODEL = str(os.environ.get('GROQ_CHAT_MODEL'))
