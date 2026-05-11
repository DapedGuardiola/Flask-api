from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    Debug = os.getenv('FLASK_DEBUG',False)
    PORT = os.getenv('FLASK_PORT',5000)