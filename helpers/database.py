from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URL"),tlsCAFile=certifi.where())
DB = client["pump_fun"]

INITIAL_STATE = DB['bonding_curve_stage']
TOKENS = DB['tokens']