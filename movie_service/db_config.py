import os

from dotenv import load_dotenv

load_dotenv()

data = {
    'name': os.environ.get('NAME'),
    'user': os.environ.get('USER'),
    'password': os.environ.get('PASS'),
    'host': os.environ.get('HOST'),
    'port': os.environ.get('PORT')
}
