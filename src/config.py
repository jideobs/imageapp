import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

S3_BUCKET = os.getenv('S3_BUCKET')
